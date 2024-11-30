""" Match related CRUD methods """
from typing import Any

from sqlmodel import Session, select

from app.models import Match, MatchCreate, MatchCreateIn, MatchUpdate

def create_match(*, session: Session, match_create: MatchCreate) -> Match:
    db_obj = Match.model_validate(match_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_match(*, session: Session, db_match: Match, match_in: MatchUpdate) -> Any:
    if match_in.local_id:
        db_match.local_id = match_in.local_id
    if match_in.visitor_id:
        db_match.visitor_id = match_in.visitor_id
    if match_in.date:
        db_match.date = match_in.date
    if match_in.price:
        db_match.price = match_in.price
    if match_in.competition_id:
        db_match.competition_id = match_in.competition_id

    session.add(db_match)
    session.commit()
    session.refresh(db_match)

    return db_match


def delete_match(*, session: Session, match_id: int) -> Any:
    match = session.get(Match, match_id)
    session.delete(match)
    session.commit()

    return match


def get_match_by_name(*, session: Session, name: str) -> Match | None:
    statement = select(Match).where(Match.name == name)
    session_match = session.exec(statement).first()

    return session_match


def get_team_home_matches(*, session: Session, team_id: int):
    statement = select(Match).where(Match.local_id == team_id)

    return session.exec(statement).all()


def get_team_away_matches(*, session: Session, team_id: int):
    statement = select(Match).where(Match.visitor_id == team_id)

    return session.exec(statement).all()

def get_match(*, session: Session, match_id: int) -> Match | None:
    return session.get(Match, match_id)