from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def get_charity_project_or_404(charity_project_id: int, session: AsyncSession) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!',
        )
    return charity_project
