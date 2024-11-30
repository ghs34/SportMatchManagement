""" Competition management routes """

from fastapi import APIRouter, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (Competition, Message,
                        CompetitionOut, CompetitionsOut,
                        CompetitionCreate, CompetitionUpdate)

router = APIRouter()


@router.get("/", response_model=CompetitionsOut)
async def read_competitions(session: SessionDep, skip: int = 0, limit: int = 10):
    query = select(Competition).offset(skip).limit(limit)
    results = session.exec(query).all()

    count_statement = select(func.count()).select_from(Competition)
    count = session.exec(count_statement).one()

    return CompetitionsOut(data=results, count=count)


@router.post("/{competition_name}", response_model=CompetitionOut)
async def create_competition(session: SessionDep, competition_in: CompetitionCreate):
    competition = crud.competition.get_competition_by_name(session=session, name=competition_in.name)
    if competition:
        raise HTTPException(status_code=400, detail=f"Competition with name {competition.name} already exists")

    competition = crud.competition.create_competition(session=session, competition_create=competition_in)

    return competition

@router.get("/{competition_name}", response_model=CompetitionOut)
async def read_competition(session: SessionDep, competition_name: str):
    competition = crud.competition.get_competition_by_name(session=session, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    return competition


@router.delete("/{competition_name}", response_model=Message)
async def delete_competition(session: SessionDep, competition_name: str):
    competition = crud.competition.get_competition_by_name(session=session, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail=f"Competition with name {competition_name} not found")
    crud.competition.delete_competition(session=session, db_competition=competition)

    return Message(message=f"Competition with name {competition_name} deleted")


@router.put("/{competition_name}", response_model=CompetitionOut)
async def update_competition(session: SessionDep, competition_in: CompetitionUpdate|CompetitionCreate):
    competition = crud.competition.get_competition_by_name(session=session, name=competition_in.name)
    if competition:
        competition = crud.competition.update_competition(session=session, db_competition=competition, competition_in=competition_in)

    else:
        competition = crud.competition.create_competition(session=session, competition_create=competition_in)

    return competition