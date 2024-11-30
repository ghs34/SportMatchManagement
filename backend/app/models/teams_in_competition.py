from sqlmodel import SQLModel, Field
from typing import Optional

class TeamCompetitionLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    competition_id: Optional[int] = Field(default=None, foreign_key="competition.id", primary_key=True)