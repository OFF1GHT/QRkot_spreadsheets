from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation, User
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.core.constants import MIN_AMOUNT


class CharityProjectService:
    def __init__(self, session):
        self.session = session

    def _validate_investments(self, charity_project: CharityProject) -> None:
        """Проверка на присутствие/отсутствие инвестиций в проекте."""
        if charity_project.invested_amount > MIN_AMOUNT:
            raise HTTPException(
                status_code=400,
                detail='Проверка на присутствие/отсутствие инвестиций в проекте',
            )

    async def charity_project_remove(self, charity_project: CharityProject):
        self._validate_investments(charity_project)
        await charity_project_crud.remove(charity_project, self.session)
        return charity_project

    async def _check_name_duplicate(self, charity_project_name: str) -> None:
        charity_project_id = await charity_project_crud.get_project_id_by_name(
            charity_project_name, self.session
        )
        if charity_project_id is not None:
            raise HTTPException(
                status_code=400, detail='Проект с таким именем уже существует!'
            )

    async def _check_project_before_update(
        self, charity_project: CharityProject, obj_in: CharityProjectUpdate
    ) -> None:
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=400, detail='Закрытый проект нельзя редактировать!'
            )
        if obj_in.full_amount:
            if obj_in.full_amount < charity_project.invested_amount:
                raise HTTPException(
                    status_code=400,
                    detail='Нельзя установить сумму меньше вложенной',
                )

    async def charity_project_create(self, charity_project: CharityProjectCreate):
        await self._check_name_duplicate(charity_project.name)
        new_charity_project = await charity_project_crud.create(
            charity_project, self.session
        )

        await self._investing_process(new_charity_project)

        return new_charity_project

    async def charity_project_update(
        self, charity_project: CharityProject, obj_in: CharityProjectUpdate
    ):
        if obj_in.name:
            await self._check_name_duplicate(obj_in.name)

        await self._check_project_before_update(charity_project, obj_in)
        charity_project = await charity_project_crud.update(
            charity_project, obj_in, self.session
        )
        return charity_project

    async def create_donation_obj(
        self, donation, user: Optional[User] = None
    ):
        new_donation = await donation_crud.create(donation, self.session, user)
        await self._investing_process(new_donation)
        return new_donation

    async def _investing_process(self, entity):
        if entity.invested_amount >= entity.full_amount:
            return

        free_amount = entity.full_amount - entity.invested_amount
        crud = Donation if isinstance(entity, CharityProject) else CharityProject
        unclosed_objects = await CRUDBase(crud).get_unclosed_objects(self.session)

        for db_object in unclosed_objects:
            amount_to_invest = min(
                free_amount, db_object.full_amount - db_object.invested_amount
            )
            db_object.invested_amount += amount_to_invest
            entity.invested_amount += amount_to_invest
            free_amount -= amount_to_invest

            if db_object.invested_amount == db_object.full_amount:
                db_object.fully_invested = True
                db_object.close_date = datetime.now()

            if free_amount == MIN_AMOUNT:
                break

        if entity.invested_amount == entity.full_amount:
            entity.fully_invested = True
            entity.close_date = datetime.now()

        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
