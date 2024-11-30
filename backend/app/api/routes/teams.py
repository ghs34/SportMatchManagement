""" Team management routes """
from fastapi import APIRouter, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import SessionDep
from app.models import Team, Message, TeamOut, TeamsOut, TeamCreate, TeamUpdate

router = APIRouter()


@router.get("/", response_model=TeamsOut)
async def read_teams(session: SessionDep, skip: int = 0, limit: int = 10):
    query = select(Team).offset(skip).limit(limit)
    results = session.exec(query).all()

    count_statement = select(func.count()).select_from(Team)
    count = session.exec(count_statement).one()

    return TeamsOut(data=results, count=count)

@router.post("/{team_name}")
async def create_team(team_data: TeamCreate, session: SessionDep):
    team = crud.team.get_team_by_name(session=session, name=team_data.name)
    if team:
        raise HTTPException(status_code=409, detail=f"Team {team.name} already exists")

    team = crud.team.create_team(session=session, team_create=team_data)

    return team

@router.get("/{team_name}", response_model=TeamOut)
async def read_team(team_name: str, session: SessionDep):
    team = crud.team.get_team_by_name(session=session, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_name} not found")

    return team


@router.delete("/{team_name}", response_model=Message)
async def delete_team(team_name: str, session: SessionDep):
    team = crud.team.get_team_by_name(session=session, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_name} not found")

    crud.team.delete_team(session=session, team_id=team.id)
    return Message(message=f"Team {team_name} deleted")


@router.put("/{team_name}")
async def update_team(team_data: TeamCreate|TeamUpdate, session: SessionDep):
    team = crud.team.get_team_by_name(session=session, name=team_data.name)
    if team: crud.team.update_team(session=session, db_team=team, team_in=team_data)
    else: team = crud.team.create_team(session=session, team_create=team_data)

    return team