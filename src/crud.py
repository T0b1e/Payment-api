from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
import src.models as models

def checkAll(db: Session): #All check
    categories_amounts = db.query(models.Transcations.category, sums(models.Transcations.amount)).group_by(models.Transcations.category).all()
    deposit_cash = db.query(models.Main.deposit, models.Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result

def checkSingle(db: Session, date: int): #Single check
    categories_amounts = db.query(models.Transcations.category, sums(models.Transcations.amount)).filter(models.Transcations.date == date).group_by(models.Transcations.category).all()
    deposit_cash = db.query(models.Main.deposit, models.Main.cash).first()
    result = {category: amount for category, amount in categories_amounts}
    result.update({ "deposit": deposit_cash[0],
                    "cash": deposit_cash[1]})  
    return result



# PaymentMethod().checkSingle()