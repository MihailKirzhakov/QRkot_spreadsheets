# C:\Dev\cat_charity_fund\app\models\base.py
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            'invested_amount >= 0', name='check_invested_amount_non_negative'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount'
        ),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, index=True)