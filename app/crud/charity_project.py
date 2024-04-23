from typing import Optional, List

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_projects_by_completion_rate(self, session: AsyncSession) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1
            ).order_by(
                extract('day', CharityProject.close_date) -
                extract('day', CharityProject.create_date)
            )
        )
        projects = projects.scalars().all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
