from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_charityproject_exists,
    check_full_amount,
    check_close_project, check_project_before_edit,
    check_project_invested_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.base import charityproject_crud, donation_crud
from app.schemas.charityproject import (
    CharityProjectDB,
    CharityProjectBase,
    CharityProjectUpdate
)
from app.services.investment import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectBase,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    new_room = await charityproject_crud.create(project, session)
    invest_project = invest_donations(
        new_room, await donation_crud.get_all_open(session)
    )
    session.add_all(invest_project)
    await session.commit()
    await session.refresh(new_room)
    return new_room


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    return await charityproject_crud.get_multi(session)


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
    charityproject_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charityproject_exists(
        charityproject_id, session)
    check_project_before_edit(update_data)
    check_close_project(project)
    if update_data.name:
        await check_name_duplicate(update_data.name, session)
    if update_data.full_amount is not None:
        await check_full_amount(
            update_data.full_amount, charityproject_id, session
        )
    return await charityproject_crud.update(project, update_data, session)


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
    charityproject_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charityproject_exists(charityproject_id, session)
    project = await charityproject_crud.remove(project, session)
    check_close_project(project)
    check_project_invested_amount(project)
    return project
