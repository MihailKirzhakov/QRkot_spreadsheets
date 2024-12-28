from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentBaseModel


class Donation(InvestmentBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{super().__repr__()}, '
            f'Donation(user_id={self.user_id}, '
            f'comment={self.comment})'
        )
