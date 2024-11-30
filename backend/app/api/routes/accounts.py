from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
from app.models import (
    Message,
    Account,
    AccountCreate,
    AccountOut,
    AccountUpdate
)

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=AccountOut)
def create_account(*, session: SessionDep, account_in: AccountCreate) -> Any:
    """
    Create a new account.
    """
    account = Account(**account_in.dict())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/", response_model=List[AccountOut])
def get_accounts(session: SessionDep) -> Any:
    """
    Get all accounts.
    """
    accounts = session.exec(select(Account)).all()
    return accounts


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, session: SessionDep) -> Any:
    """
    Get a single account by ID.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, account_in: AccountUpdate, session: SessionDep) -> Any:
    """
    Update an account.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    for key, value in account_in.dict(exclude_unset=True).items():
        setattr(account, key, value)

    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.delete("/{account_id}", response_model=AccountOut)
def delete_account(account_id: int, session: SessionDep) -> Any:
    """
    Delete an account.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    session.delete(account)
    session.commit()
    return account