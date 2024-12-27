# C:\Dev\cat_charity_fund\app\models\charity_project.py
from sqlalchemy import Column, String, Text

from app.constants.constants import ConstantNumbers
from app.models.base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):
    name = Column(
        String(ConstantNumbers.MAX_NAME_LENGTH), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date}'
            f'CharityProject(name={self.name}, '
            f'description={self.description[:20]}...)'
        )
