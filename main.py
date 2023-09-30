from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from sqlalchemy.orm import Session
from src.crud import checkAll, checkSingle, addExpense, addIncome, transfer_between_wallets
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


@app.post("/expense/{types}")
async def expense(
    wallet_name: str,
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    if token in api_key:
        value = addExpense(db=db, types=types, wallet_id=wallet_name , amount=money, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")


@app.post("/income/{types}")
async def income(
    wallet_name: str,
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):
    if token in api_key:
        value = addIncome(db=db, types=types, wallet_id=wallet_name , amount=money, description=description)
        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        return {"date": presentDate, 
                "value": value}

    raise HTTPException(status_code=404, detail="Invalid API keys")


@app.post("/transfer")
async def transfer_funds(
    origin_wallet_name: str,
    destination_wallet_name: str,
    amount: float,
    description: str = None,
    token: str = Query(default=None, max_length=50),
    db: Session = Depends(get_db)
):
    if token and token not in api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    transfer_result = transfer_between_wallets(
        db =  db,
        origin_wallet_name      = origin_wallet_name,
        destination_wallet_name = destination_wallet_name,
        amount =  amount,
        description =  description
    )

    if transfer_result: # adding return origin value and destination value
        return {"message": "Transfer successful", "transaction_id": transfer_result.id}
    else:
        raise HTTPException(status_code=400, detail="Transfer failed")

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# https://script.google.com/macros/s/AKfycbxbMCAhYnnLsf-MzcyNJmBxnSHWWAxNKtgXMX5ONEU3gbrAxRdGBABYN0ojViAi_wwI/exec