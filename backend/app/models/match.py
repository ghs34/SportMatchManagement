""" Match models """
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime


# Shared properties
class MatchBase(SQLModel):
    date: datetime
    price: float
    total_available_tickets: int


# Database model, database table inferred from class name
class Match(MatchBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    local_id: int = Field(foreign_key="team.id", nullable=False)
    local: "Team" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Match.local_id]"})

    visitor_id: int = Field(foreign_key="team.id", nullable=False)
    visitor: "Team" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Match.visitor_id]"})

    competition_id: int = Field(foreign_key="competition.id", nullable=False)
    competition: "Competition" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Match.competition_id]"})

    orders: list["Order"] = Relationship(back_populates="match")


# Properties to receive via API on creation
class MatchCreate(MatchBase):
    local_id: int
    visitor_id: int
    competition_id: int
    date: datetime
    price: float
    total_available_tickets: int


class MatchCreateIn(MatchBase):
    local_team: str
    visitor_team: str
    competition: str
    date: datetime
    price: float
    total_available_tickets: int


# Properties to receive via API on update, all are optional
class MatchUpdate(MatchBase):
    date: datetime | None = None
    price: float | None = None
    local_id: int | None = None
    visitor_id: int | None = None
    competition_id: int | None = None
    total_available_tickets: int | None = None

class MatchUpdateIn(MatchBase):
    date: datetime | None = None
    price: float | None = None
    local_team: str | None = None
    visitor_team: str | None = None
    competition: str | None = None
    total_available_tickets: int | None = None


# Properties to return via API, id is always required
class MatchOut(MatchBase):
    id: int
    date: datetime
    price: float
    local_team: str
    visitor_team: str
    competition_id: int
    total_available_tickets: int


class MatchesOut(SQLModel):
    data: list[MatchOut]
    count: int


class Message(SQLModel):
    message: str