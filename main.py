from fastapi import FastAPI, Depends, HTTPException
from src.crud import checkAll, checkSingle, addExpense, addIncome, toBangkok, toSCB
from src.database import SessionLocal, engine
import src.models as models

# Third party
from datetime import datetime
from typing import Union
from sqlalchemy.orm import Session

app = FastAPI()

# Header and Encrupt
timeNow = datetime.now()
presentDate = timeNow.strftime("%Y-%m-%d")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "It's Working fine"}

@app.get("/check")
async def checks(db: Session = Depends(get_db)):
    return {"date": f'2023-01-01 --> {presentDate}',
            "value": checkAll(db)}

@app.get("/check/{date}")
async def check(date : str, db: Session = Depends(get_db)):
    return {"date": date,
            "value": checkSingle(db, date=date)}

@app.post("/expense/{types}/{money}")
async def expense(
    money: float, 
    types: str, 
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    value = addExpense(db=db, amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate, 
            "value": value}

@app.post("/income/{types}/{money}")
async def income(
    money: float, 
    types: str, 
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    value = addIncome(db=db, amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate, 
            "value": value}

@app.post("/transactionsToBnk/{types}/{money}")
async def transactionsToBnk(
    money: float, 
    types: str, 
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    value = toBangkok(db=db, amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate, 
            "value": value}

@app.post("/transactionsToSCB/{types}/{money}")
async def transactionsToSCB(
    money: float, 
    types: str, 
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    value = toSCB(db=db, amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate, 
            "value": value}