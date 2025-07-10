from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(gt=1)
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDBfull(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDBpart(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
