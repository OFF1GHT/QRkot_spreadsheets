from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import MIX_PROJECT_NAME_LEN, MAX_PROJECT_NAME_LEN


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=MIX_PROJECT_NAME_LEN, max_length=MAX_PROJECT_NAME_LEN)
    description: Optional[str] = Field(None, min_length=MIX_PROJECT_NAME_LEN)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=MIX_PROJECT_NAME_LEN, max_length=MAX_PROJECT_NAME_LEN)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
