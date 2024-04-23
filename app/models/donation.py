from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        Integer, Text)

from app.core.db import Base
from app.core.constants import MIN_AMOUNT


class Donation(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
    full_amount = Column(Integer(), CheckConstraint(f'full_amount > {MIN_AMOUNT}'))
    invested_amount = Column(Integer, default=MIN_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
