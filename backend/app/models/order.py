from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from typing import Optional
from .match import Match
from .account import Account

class OrderBase(SQLModel):
    tickets_bought: int

class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="match.id")
    account_id: int = Field(foreign_key="account.id")
    match: Match = Relationship(back_populates="orders")
    account: Account = Relationship(back_populates="orders")

class OrderCreate(SQLModel):
    tickets_bought: int
    match_id: int
    account_id: int

class OrderUpdate(SQLModel):
    tickets_bought: Optional[int] = None
    match_id: Optional[int] = None
    account_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    tickets_bought: int
    match_id: int
    account_id: int
    match_date: date
    visitor_team_name: str
    local_team_name: str
    user_email: str

class OrdersOut(SQLModel):
    data: list[OrderOut]
    count: int