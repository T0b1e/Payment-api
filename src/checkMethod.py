from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
from src.models import Main, TransactionsTable
from datetime import date


def checkAll(db: Session):  #All check
    categories_amounts = db.query(TransactionsTable.category, sums(TransactionsTable.amount)).group_by(TransactionsTable.category).all()
    deposit_cash = db.query(Main.deposit, Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result


def checkSingle(db: Session, date: int):  #Single check
    categories_amounts = db.query(TransactionsTable.category, sums(TransactionsTable.amount)).filter(TransactionsTable.date == date).group_by(TransactionsTable.category).all()
    deposit_cash = db.query(Main.deposit, Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result


def checkWalletBalance(db: Session, wallet_name: str):
    deposit = (
        db.query(
            Main.deposit
        )
        .filter(Main.name == wallet_name)
        .group_by(Main.name)
        .first()
    )

    if deposit:
        return {"wallet_name": wallet_name, "cash_sum": deposit[0]}

    return {"wallet_name": wallet_name, "cash_sum": 0}


def checkAllWalletBalance(db: Session):  # Use date as a string
    all_wallet_balances = (
        db.query(Main.name, Main.deposit)
        .group_by(Main.name)
        .all()
    )

    result = {}
    for wallet_name, cash_sum in all_wallet_balances:
        result[wallet_name] = cash_sum

    return result


def checkTransactions(db: Session, date: str = date.today().isoformat()):
    transaction_results = (
        db.query(TransactionsTable.types, TransactionsTable.amount)
        .filter(TransactionsTable.date == date)
        .group_by(TransactionsTable.types)
        .all()
    )

    result = {}
    for wallet_name, cash_sum in transaction_results:
        result[wallet_name] = cash_sum

    return result


