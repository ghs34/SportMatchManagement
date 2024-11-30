import enum
#from models_dades import sports_list, categories_list
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class CompetitionBase(BaseModel):
    name: str
    category: enum.Enum('category',dict(zip(categories_list,categories_list)))
    sport:  enum.Enum('sport',dict(zip(sports_list,sports_list)))


class CompetitionCreate(CompetitionBase):
    pass


class Competition(CompetitionBase):
    id: int
    teams: list[Team] = []

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    date: datetime
    price: float
    local: TeamBase
    visitor: TeamBase
    competition: CompetitionBase


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    local: Team
    visitor: Team
    competition: Competition
    total_available_tickets: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    match: Match
    tickets_bought: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    available_money: float


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    orders: list[Order] = []

    class Config:
        orm_mode = True