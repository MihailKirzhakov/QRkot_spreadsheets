# C:\Dev\cat_charity_fund\app\models\charity_project.py
from sqlalchemy import Column, String, Text

from app.constants.constants import ConstantNumbers
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(
        String(ConstantNumbers.MAX_NAME_LENGTH), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)
