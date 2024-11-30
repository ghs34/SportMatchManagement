""" Competition related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from app.models import Competition, CompetitionCreate, CompetitionUpdate, MatchesOut

def create_competition(*, session: Session, competition_create: CompetitionCreate) -> Competition:
    db_obj = Competition.model_validate(competition_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_competition(*, session: Session, db_competition: Competition, competition_in: CompetitionUpdate) -> Any:
    if competition_in.teams:
        db_competition.teams = competition_in.teams
    if competition_in.name:
        db_competition.name = competition_in.name
    if competition_in.category:
        db_competition.category = competition_in.category

    session.add(db_competition)
    session.commit()
    session.refresh(db_competition)

    return db_competition


def delete_competition(*, session: Session, db_competition: Competition) -> Any:
    session.delete(db_competition)
    session.commit()


def get_competition_by_name(*, session: Session, name: str) -> Competition | None:
    statement = select(Competition).where(Competition.name == name)
    session_competition = session.exec(statement).first()

    return session_competition

def get_competition_matches(*, session: Session, competition_name: str) -> MatchesOut | None:
    statement = select(Competition).where(Competition.name == competition_name)
    session_competition = session.exec(statement).first()

    if not session_competition:
        # If there's no competition with the given name, return None or empty list
        return None

    if session_competition.matches is None:
        return list([])

    return session_competition.matches
