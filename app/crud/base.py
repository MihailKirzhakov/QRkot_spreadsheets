# C:\Dev\cat_charity_fund\app\crud\base.py
from typing import Optional, TypeVar, Generic, List, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, CharityProject, Donation
from app.schemas.charityproject import CharityProjectUpdate
from app.schemas.donation import DonationCreate

ModelType = TypeVar('ModelType')


class CRUDBase(Generic[ModelType]):

    def __init__(self, model: ModelType):
        self.model = model

    async def get(
        self,
        data_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        return (await session.execute(
            select(self.model).where(
                self.model.id == data_id
            )
        )).scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ) -> list[ModelType]:
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
        self,
        data: DonationCreate,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> Donation:
        create_data = data.dict()
        if user:
            create_data['user_id'] = user.id
        db_data = self.model(**create_data)
        session.add(db_data)
        await session.flush()
        await session.refresh(db_data)
        return db_data

    async def update(
        self,
        db_data: CharityProject,
        data: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        encode_data = jsonable_encoder(db_data)
        update_data = data.dict(exclude_unset=True)

        for field in encode_data:
            if field in update_data:
                setattr(db_data, field, update_data[field])
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)
        return db_data

    async def remove(
        self,
        db_data: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_data)
        await session.commit()
        return db_data

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )).scalars().first()

    async def get_all_open(
        self,
        session: AsyncSession,
    ) -> list:
        return (
            await session.execute(
                select(self.model).filter(
                    self.model.fully_invested == 0
                ).order_by(asc(self.model.create_date))
            )
        ).scalars().all()

    async def get_by_filter(
            self,
            session: AsyncSession,
            filter_field: str,
            filter_value: int,
    ) -> list[ModelType]:
        return (await session.execute(
            select(self.model).where(
                getattr(self.model, filter_field) == filter_value
            )
        )).scalars().all()

    async def save_changes(
        self, session: AsyncSession, objects: ModelType
    ) -> None:
        session.add_all(objects)
        await session.commit()

    async def get_objects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> List[Dict[str, str]]:
        return await session.execute(
            select([self.model]).where(self.model.fully_invested == 1)
        ).scalars().all()


charityproject_crud = CRUDBase(CharityProject)
donation_crud = CRUDBase(Donation)
