# C:\Dev\cat_charity_fund\app\models\donation.py
from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentBaseModel


class Donation(InvestmentBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date}'
            f'Donation(user_id={self.user_id}, '
            f'comment={self.comment})'
        )
