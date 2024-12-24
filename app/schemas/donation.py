from datetime import datetime
from typing import Optional

from pydantic import Field, StrictBool, BaseModel

from app.constants.constants import ConstantNumbers
from .charityproject import NonNegativeInt


class DonationCreate(BaseModel):
    full_amount: NonNegativeInt = Field(
        example=ConstantNumbers.EXAMPLE_AMOUNT
    )
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationDB):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: StrictBool
    close_date: Optional[datetime]
