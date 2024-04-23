from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Integer,
                        String, Text)

from app.core.db import Base
from app.core.constants import MIN_AMOUNT, MAX_PROJECT_NAME_LEN


class CharityProject(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(MAX_PROJECT_NAME_LEN), unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer(), CheckConstraint(f'full_amount > {MIN_AMOUNT}'))
    invested_amount = Column(Integer, default=MIN_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
