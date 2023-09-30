from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
from src.models import Main, TranscationsTable, IncomeTable, ExpenseTable
from datetime import datetime, date


def checkAll(db: Session):  #All check
    categories_amounts = db.query(TranscationsTable.category, sums(TranscationsTable.amount)).group_by(TranscationsTable.category).all()
    deposit_cash = db.query(Main.deposit, Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result


def checkSingle(db: Session, date: int):  #Single check
    categories_amounts = db.query(TranscationsTable.category, sums(TranscationsTable.amount)).filter(TranscationsTable.date == date).group_by(TranscationsTable.category).all()
    deposit_cash = db.query(Main.deposit, Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result



def addExpense(db: Session, wallet_name: str, amount: float, types: str, description: str): #expense 

    main_info = db.query(Main.name, Main.deposit).filter(Main.name == wallet_name).first()

    if main_info:
        wallet_name, deposit = main_info

        if deposit >= amount:
            db.query(Main).filter(Main.name == wallet_name).update({Main.deposit: Main.deposit - amount})
            db.commit()

            data = ExpenseTable(
                date=date.today(),
                time=datetime.now().time(),
                category=types,
                wallet_id = wallet_name,
                amount=amount,
                description=description
            )

            db.add(data)
            db.commit()
            db.refresh(data)
            
            return data
        else:
            return None

    return None



def addIncome(db: Session, amount: float, types: str, description: str): #expense 

    main_info = db.query(Main.name, Main.deposit).filter(Main.name == wallet_name).first()

    if main_info:
        wallet_name, deposit = main_info

        if deposit >= amount:
            db.query(Main).filter(Main.name == wallet_name).update({Main.deposit: Main.deposit + amount})
            db.commit()

            data = IncomeTable(
                date=date.today(),
                time=datetime.now().time(),
                category=types,
                wallet_id = wallet_name,
                amount=amount,
                description=description
            )

            db.add(data)
            db.commit()
            db.refresh(data)
            
            return data
        else:
            return None

    return None

        

def transfer_between_wallets(db: Session, origin_wallet_name: str, destination_wallet_name: str, amount: float, description: str):

    origin_wallet = db.query(Main.deposit).filter(Main.name == origin_wallet_name).first()
    destination_wallet = db.query(Main.deposit).filter(Main.name == destination_wallet_name).first()

    if origin_wallet and destination_wallet:

        db.query(Main).filter(Main.name == origin_wallet_name).update({Main.deposit: origin_wallet - amount})
        db.query(Main).filter(Main.name == destination_wallet_name).update({Main.deposit: destination_wallet + amount})
        db.commit()

        data = TranscationsTable(
            date=date.today(),
            time=datetime.now().time(),
            category="Transfer",
            amount=amount,
            cash=origin_wallet - amount,
            deposit=origin_wallet,
            description=description
        )

        db.add(data)
        db.commit()
        db.refresh(data)

        return data
    else:
        return None


