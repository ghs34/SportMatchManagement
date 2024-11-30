""" Main API routes definition """
from fastapi import APIRouter

from app.api.routes import login, users, utils, teams, competitions, matches, orders, accounts

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(competitions.router, prefix="/competitions", tags=["competitions"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
