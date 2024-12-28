from sqlalchemy import Column, String, Text

from app.constants.constants import MAX_NAME_LENGTH
from app.models.base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):
    name = Column(
        String(MAX_NAME_LENGTH), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{super().__repr__()}, '
            f'CharityProject(name={self.name}, '
            f'description={self.description[:20]}...)'
        )
