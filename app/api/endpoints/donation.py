# C:\Dev\cat_charity_fund\app\api\endpoints\donation.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.user import current_user
from app.crud.base import donation_crud, charityproject_crud
from app.models import User
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationDBSuperuser
)
from app.services.investment import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    targets = await charityproject_crud.get_all_open(session)
    invest_donation = invest_donations(
        new_donation, targets
    )
    await donation_crud.save_changes(session, new_donation, invest_donation)
    await session.refresh(invest_donation)
    return invest_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_by_filter(session, 'user_id', user.id)


@router.get(
    '/',
    response_model=list[DonationDBSuperuser],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)
