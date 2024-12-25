from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.base import charityproject_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value,
    get_projects_by_duration
)

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charityproject_crud.get_projects_by_completion_rate(
        session
    )
    duration_projects = await get_projects_by_duration(projects)
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            duration_projects,
            wrapper_services
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=error)
    return print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
