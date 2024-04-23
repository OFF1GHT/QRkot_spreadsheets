from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.charity_project import CharityProjectService

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def post_charity_projects(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    if not charity_project.description:
        raise HTTPException(
            status_code=422, detail='Описание проекта обязательно'
        )

    charity_project_service = CharityProjectService(session)
    print(session)

    new_project = await charity_project_service.charity_project_create(charity_project)

    return new_project


@router.get(
    '/',
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_project = await charity_project_crud.get_multi(session)
    return all_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project_service = CharityProjectService(session)
    charity_project = await charity_project_service.charity_project_update(
        project_id, obj_in
    )
    return charity_project


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление благотворительного проекта. Доступно для суперюзеров."""
    charity_project_service = CharityProjectService(session)
    charity_project = await charity_project_service.charity_project_remove(
        project_id
    )
    return charity_project
