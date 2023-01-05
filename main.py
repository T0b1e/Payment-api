from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from sqlalchemy.orm import Session
from src.crud import checkAll, checkSingle, addExpense, addIncome, toBangkok, toSCB
from src.database import SessionLocal, engine
import src.models as models

# Third party
from datetime import datetime
from typing import Union

import dotenv
import os

from pydantic import Required

dotenv.load_dotenv('./src/keys.env')
api_key = os.getenv('API_KEY')

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
async def checks(db: Session = Depends(get_db), token: Union[str, None] = Query(default=Required, max_length=50)):
    if token in api_key:
        value = checkAll(db)
        if value:
            return {"date": f'2023-01-01 --> {presentDate}',
                    "value": value}
        raise HTTPException(status_code=404, detail="Didn't has Value yet")
    raise HTTPException(status_code=404, detail="Invalid API keys")

@app.get("/check/{date}")
async def check(date : str, db: Session = Depends(get_db), token: Union[str, None] = Query(default=Required, max_length=50)):
    if token in api_key:
        value = checkAll(db)
        if value:
            return {"date": date,
                    "value": value}
        raise HTTPException(status_code=404, detail="Didn't has Value yet")
    raise HTTPException(status_code=404, detail="Invalid API keys")

@app.post("/expense/{types}/{money}")
async def expense(
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):
    
    if token in api_key:
        value = addExpense(db=db, amount=money, types=types, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")

@app.post("/income/{types}/{money}")
async def income(
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):
    if token in api_key:
        value = addIncome(db=db, amount=money, types=types, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")

@app.post("/transactionsToBnk/{types}/{money}")
async def transactionsToBnk(
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):
    if token in api_key:
        value = toBangkok(db=db, amount=money, types=types, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")

@app.post("/transactionsToSCB/{types}/{money}")
async def transactionsToSCB(
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):
    if token in api_key:
        value = toSCB(db=db, amount=money, types=types, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)