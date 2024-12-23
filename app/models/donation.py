# C:\Dev\cat_charity_fund\app\models\donation.py
from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
