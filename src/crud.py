from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
import src.models as models

def checkAll(db: Session): #Single check
    return db.query(models.Transcations).all()

def checkSingle(db: Session, date: int): #Single check
    # data = db.query(models.Transcations.category, sum(models.Transcations.amount)).with_entities(models.Transcations.amount).filter(models.Transcations.date == date).group_by(models.Transcations.category).all()
    expense = db.query(models.Transcations.category, sums(models.Transcations.amount)).filter(models.Transcations.date == date)  .group_by(models.Transcations.category).all()
    strorage = db.query(models.Main.deposit, models.Main.cash).first()
    withoutDepo = {category: amount for category, amount in expense}
    withoutDepo.update(
                        {   "deposit": strorage[0][0],
                            "cash": strorage[0][1]})  
    return withoutDepo



# PaymentMethod().checkSingle()