from fastapi import FastAPI, Depends, HTTPException
from src.crud import PaymentMethod
from typing import Union

# Third party
from datetime import datetime

app = FastAPI()

# Header and Encrupt
timeNow = datetime.now()
presentDate = timeNow.strftime("%Y-%m-%d")

@app.get("/")
async def root():
    return {"message": "It's Working fine"}

@app.get("/check")
async def checks():
    return {"value": PaymentMethod().checkAll()}

@app.get("/check/{date}")
async def check(date : str):
    return {"date": date,
            "value": PaymentMethod().checkSingle(date=date)}

@app.post("/expense/{types}/{money}")
async def expense(types: str, money: float, description: Union[str, None] = None):
    value = PaymentMethod().expense(amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate, 
            "value": value}

@app.post("/income/{types}/{money}")
async def income(types: str, money: float, description: Union[str, None] = None):
    value = PaymentMethod().income(amount=money, types=types, description=description)
    if not value:
        raise HTTPException(status_code=404, detail="Error :(")

    return {"date": presentDate,
            "value": value}

@app.post("/transactions/{types}/{money}")
async def transactions(types: str, money: float, description: Union[str, None] = None):
    return {"date": presentDate,
            "value": PaymentMethod().transactions(amount=money, types=types, description=description)}
