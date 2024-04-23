from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationAdminDB,
    DonationBase,
    DonationCreate,
    DonationDB
)
from app.services.charity_project import CharityProjectService

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation_service = CharityProjectService(session)
    new_donation = await donation_service.create_donation_obj(donation, user)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation_superuser(
    session: AsyncSession = Depends(get_async_session),
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations