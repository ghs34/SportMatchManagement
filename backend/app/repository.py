from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func

import app.models
import models


def check_money_to_buy(db: Session, account: models.Account, order: models.Order) -> bool:
    return account.available_money >= (order.match.price * order.tickets_bought)

def check_tickets_available(db: Session, match: models.Match) -> bool:
    return match.total_available_tickets > 0

def update_available_tickets(db: Session, order: models.Order):
    match = order.match
    total_available_tickets = match.total_available_tickets - order.tickets_bought

    db_match = db.query(models.Match).filter(models.Match.id == match.id).first()

    if db_match:
        db_match.total_available_tickets = total_available_tickets
        db.commit()
        db.refresh(db_match)
        return db_match
    else:
        return None

def update_account(db: Session, account: models.Account, order: models.Order):
    available_money = account.available_money - (order.tickets_bought * order.match.price)

    # Query the account from the database
    db_account = db.query(models.Account).filter(models.Account.id == account.id).first()

    if db_account:
        # Update the available money in the account
        db_account.available_money = available_money

        # Commit the changes to the database
        db.commit()
        db.refresh(db_account)

        return db_account
    else:
        return None

def add_order_to_account(db: Session, account: models.Account, new_order: models.Order):

    db_account = db.query(models.Account).filter(models.Account.id == account.id).first()

    if db_account:
        db_account.orders.append(new_order)
        db.commit()
        db.refresh(db_account)

        return db_account
    else:
        return None

def save_changes(db: Session, account: models.Account, order: models.Order, match: models.Match):
    try:

        db.begin()
        db.add(order)
        db.add(match)
        db.add(account)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise e