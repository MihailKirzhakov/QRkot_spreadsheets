from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import charityproject_crud
from app.models import CharityProject
from app.constants.constants import ConstantFailPhrases


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ConstantFailPhrases.PROJECT_NAME_EXISTS,
        )


async def check_charityproject_exists(
        charityproject_id: int, session: AsyncSession, ) -> CharityProject:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ConstantFailPhrases.PROJECT_NOT_FOUND
        )
    return charityproject


async def check_full_amount(
        full_amount: int,
        charityproject_id: int,
        session: AsyncSession,
) -> None:
    charityproject = await charityproject_crud.get(charityproject_id, session)
    if full_amount < charityproject.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ConstantFailPhrases.LESS_REQUIERED_AMOUNT
        )


def check_close_project(project):
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ConstantFailPhrases.EDIT_DELETE_CLOSED_PROJECT
        )


def check_project_invested_amount(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ConstantFailPhrases.DELETE_DEPOSITED_PROJECT
        )


def check_project_before_edit(project):
    if project.invested_amount is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ConstantFailPhrases.CHANGE_INVESTMENT_AMOUNT
        )
    if project.create_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ConstantFailPhrases.CHANGE_CREATION_DATE
        )

    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ConstantFailPhrases.CHANGE_CLOSING_DATE
        )

    if project.fully_invested is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ConstantFailPhrases.CHANGE_INVESTMENT_AMOUNT
        )
