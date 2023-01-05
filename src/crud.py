from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
from src.models import Main, TranscationsTable
from datetime import datetime, date

currenDate_Time = datetime.now()
currentTime = currenDate_Time.strftime('%H:%M:%S')
currentDate = currenDate_Time.strftime('%Y-%m-%d')

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

def addExpense(db: Session, amount: float, types: str, description: str): #expense 
    db.query(Main).update({Main.cash: Main.cash - amount}) # Update Cash Value
    deposit_cash = db.query(Main.deposit, Main.cash).first()  # Get old cash value

    timeNow = datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S').time()

    data = TranscationsTable(
                date=date.today(),
                time=timeNow,
                category=types, 
                amount=amount , 
                cash=deposit_cash[1], 
                deposit=deposit_cash[0], 
                description=description)

    db.add(data)
    db.commit()
    db.refresh(data)

    return data

