from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from app.models import TeamCompetitionLink, Team


class CategoryEnum(str, Enum):
    Infantil = "Infantil"
    Cadet = "Cadet"
    Juvenil = "Juvenil"
    Amateur = "Amateur"
    Professional = "Professional"

class SportEnum(str, Enum):
    Futbol = "Futbol"
    Basquet = "Basquet"
    Tenis = "Tenis"

# Shared properties
class CompetitionBase(SQLModel):
    name: str
    category: CategoryEnum
    sport: SportEnum

# Database model, database table inferred from class name
class Competition(CompetitionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="competitions", link_model=TeamCompetitionLink)

# Properties to receive via API on creation
class CompetitionCreate(CompetitionBase):
    pass

# Properties to receive via API on update, all are optional
class CompetitionUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[CategoryEnum] = None
    sport: Optional[SportEnum] = None
    teams: Optional[List[Team]] = None

# Properties to return via API, id is always required
class CompetitionOut(CompetitionBase):
    id: int
    teams: List["Team"]


class CompetitionsOut(SQLModel):
    data: List[CompetitionOut]
    count: int

class Message(SQLModel):
    message: str