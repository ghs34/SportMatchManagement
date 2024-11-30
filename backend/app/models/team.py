""" Teams models """
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from app.models.teams_in_competition import TeamCompetitionLink


# Shared properties
class TeamBase(SQLModel):
    name: str
    country: str
    description: Optional[str] = None

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    competitions: List["Competition"] = Relationship(back_populates="teams", link_model=TeamCompetitionLink)

# Properties to receive via API on creation
class TeamCreate(TeamBase):
    pass

class TeamCreateOpen(SQLModel):
    name: str
    country: str
    description: Optional[str] = None

# Properties to receive via API on update, all are optional
class TeamUpdate(TeamBase):
    name: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None

# Properties to return via API, id is always required
class TeamOut(TeamBase):
    id: int

class TeamsOut(SQLModel):
    data: List[TeamOut]
    count: int

class Message(SQLModel):
    message: str