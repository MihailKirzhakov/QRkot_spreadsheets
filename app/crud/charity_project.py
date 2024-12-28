from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )).scalars().first()


charity_crud = CRUDCharityProject(CharityProject)
