""" Team related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from app.models import Team, TeamCreate, TeamUpdate


def create_team(*, session: Session, team_create: TeamCreate) -> Team:
    db_obj = Team.model_validate(team_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_team(*, session: Session, db_team: Team, team_in: TeamUpdate) -> Any:
    if team_in.name:
        db_team.name = team_in.name
    if team_in.country:
        db_team.country = team_in.country
    if team_in.description:
        db_team.description = team_in.description

    session.add(db_team)
    session.commit()
    session.refresh(db_team)

    return db_team


def delete_team(*, session: Session, team_id: int) -> Any:
    team = session.get(Team, team_id)
    session.delete(team)
    session.commit()

    return team


def get_team_by_name(*, session: Session, name: str) -> Team | None:
    statement = select(Team).where(Team.name == name)
    session_team = session.exec(statement).first()

    return session_team