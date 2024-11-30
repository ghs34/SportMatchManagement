from sqlmodel import Field, SQLModel, Relationship
from datetime import date

class AccountBase(SQLModel):
    available_money: float

class Account(AccountBase, table=True):
    id: int = Field(default=None, primary_key=True, foreign_key="user.id")
    orders: list["Order"] = Relationship(back_populates="account")
    user: "User" = Relationship(back_populates="account")

class AccountCreate(SQLModel):
    id: int
    available_money: float

class AccountUpdate(SQLModel):
    id: int
    available_money: float

class AccountOut(SQLModel):
    id: int
    available_money: float
