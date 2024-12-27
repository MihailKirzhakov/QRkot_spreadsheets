from datetime import datetime
from typing import Optional

from pydantic import Field, StrictBool, BaseModel, validator

from app.constants.constants import ConstantNumbers, ConstantFailPhrases


class NonNegativeInt(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, int) or (value < 0):
            raise ValueError(ConstantFailPhrases.VALLUE_AMOUNT)
        return value


class CharityProjectBase(BaseModel):
    name: str = Field(
        min_length=ConstantNumbers.MIN_NAME_LENGTH,
        max_length=ConstantNumbers.MAX_NAME_LENGTH,
    )
    description: str = Field(min_length=ConstantNumbers.MIN_NAME_LENGTH)
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
                raise ValueError(ConstantFailPhrases.NAME_REQUIRED)
            elif field.name == 'description':
                raise ValueError(ConstantFailPhrases.DESCRIPTION_REQUIRED)
            elif field.name == 'full_amount':
                raise ValueError(ConstantFailPhrases.AMOUNT_REQUIRED)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(
        example=ConstantNumbers.EXAMPLE_AMOUNT
    )
    fully_invested: StrictBool = Field(example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
