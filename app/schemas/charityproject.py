from datetime import datetime
from typing import Optional

from pydantic import Field, StrictBool, BaseModel, validator

from app.constants.constants import (
    AMOUNT_REQUIRED, DESCRIPTION_REQUIRED, EXAMPLE_AMOUNT,
    MAX_NAME_LENGTH, MIN_NAME_LENGTH, NAME_REQUIRED, VALLUE_AMOUNT
)


class NonNegativeInt(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, int) or (value < 0):
            raise ValueError(VALLUE_AMOUNT)
        return value


class CharityProjectBase(BaseModel):
    name: str = Field(
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: str = Field(min_length=MIN_NAME_LENGTH)
    full_amount: NonNegativeInt


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[NonNegativeInt]
    invested_amount: Optional[NonNegativeInt]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[StrictBool]

    @validator('name', 'description', 'full_amount', allow_reuse=True)
    def field_cannot_be_null(cls, value, field):
        if not value:
            if field.name == 'name':
                raise ValueError(NAME_REQUIRED)
            elif field.name == 'description':
                raise ValueError(DESCRIPTION_REQUIRED)
            elif field.name == 'full_amount':
                raise ValueError(AMOUNT_REQUIRED)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(
        example=EXAMPLE_AMOUNT
    )
    fully_invested: StrictBool = Field(example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
