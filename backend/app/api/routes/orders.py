from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select, and_

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.models import (
    Message,
    Order,
    User,
    Account,
    OrderCreate,
    OrderOut,
    OrdersOut,
    Match,
    OrderUpdate  # Asegúrate de tener este modelo de actualización
)

router = APIRouter()

@router.get("/", response_model=List[Order])
def get_orders(session: SessionDep) -> Any:
    """
    Retrieve all orders.
    """
    orders = session.exec(select(Order)).all()
    return orders

@router.post("/{username}", response_model=Order)
def post_order(session: SessionDep, order_in: OrderCreate) -> Any:
    account = session.exec(select(Account).where(Account.id == order_in.account_id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    match = session.query(Match).filter(Match.id == order_in.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    order = Order.from_orm(order_in)
    order.account_id = account.id

    if not check_money_to_buy(session, account, order):
        raise HTTPException(status_code=400, detail="Insufficient funds")

    if not check_available_tickets(session=session, order=order_in):
        raise HTTPException(status_code=400, detail="Insufficient available tickets")

    session.add(order)
    session.commit()
    session.refresh(order)

    update_account(session=session, order_id=order.id)
    add_order_to_account(session=session, order_id=order.id)

    return order

@router.get("/{username}", response_model=List[Order])
def get_orders_user(session: SessionDep, username: str) -> Any:
    """
    Retrieve orders of account of user with username {username}.
    """
    user = session.exec(select(User).where(User.email == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account = session.exec(select(Account).where(Account.id == user.id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    orders = session.exec(select(Order).where(Order.account_id == account.id)).all()
    return orders


@router.put("/{order_id}", response_model=Order)
def update_order(session: SessionDep, order_id: int, order_in: OrderUpdate) -> Any:
    """
    Update an existing order.
    """
    order = session.exec(select(Order).where(Order.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_data = order.dict(exclude_unset=True)
    for key, value in order_in.dict(exclude_unset=True).items():
        setattr(order, key, value)

    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@router.delete("/{order_id}", response_model=Order)
def delete_order(session: SessionDep, order_id: int) -> Any:
    """
    Delete an existing order.
    """
    order = session.exec(select(Order).where(Order.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    session.delete(order)
    session.commit()
    return order


def check_money_to_buy(session: SessionDep, account: Account, order: OrderCreate) -> bool:

    statement = select(Match).where(Match.id == order.match_id)
    match = session.exec(statement).first()
    return account.available_money > (order.tickets_bought * match.price)


def check_available_tickets(session: SessionDep, order: OrderCreate) -> bool:
    statement = select(Match).where(Match.id == order.match_id)
    match = session.exec(statement).first()
    return match.total_available_tickets >= order.tickets_bought


def update_available_tickets(session: SessionDep, order_id: int):
    statement = select(Order).where(Order.id == order_id)
    order = session.exec(statement).first()
    match = order.match
    match.total_available_tickets -= order.tickets_bought
    return match


def update_account(session: SessionDep, order_id: int):
    statement = select(Order).where(Order.id == order_id)
    order = session.exec(statement).first()
    account = order.account
    account.available_money -= (order.tickets_bought * order.match.price)
    session.add(account)
    session.commit()
    return order.account


def add_order_to_account(*, session: SessionDep, order_id: int):
    statement = select(Order).where(Order.id == order_id)
    order = session.exec(statement).first()
    order.account.orders.append(order)
    return order.account