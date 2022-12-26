from fastapi import FastAPI
from src.crud import PaymentMethod
from typing import Union

app = FastAPI()

# Header and Encrupt

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check")
async def checks():
    return {"value": PaymentMethod().checkAll()}

@app.get("/check/{date}")
async def check(date : str):
    return {"date": date,
            "value": PaymentMethod().checkSingle(date=date)}

@app.post("/expense/{date}/{types}/{money}")
async def expense(date: str, types: str, money: float, description: Union[str, None] = None):
    return {"date": date,
            "value": PaymentMethod().expense(date=date, time='00:00', amount=money, types=types, description=description)}

@app.post("/income/{date}/{types}/{money}")
async def income(date: str, types: str, money: float, description: Union[str, None] = None):
    return {"date": date,
            "value": PaymentMethod().expense(date=date, time='00:00', amount=money, types=types, description=description)}

@app.post("/transactions/{date}/{types}/{money}")
async def transactions(date: str, types: str, money: float, description: Union[str, None] = None):
    return {"date": date,
            "value": PaymentMethod().expense(date=date, time='00:00', amount=money, types=types, description=description)}


'''
checks
sum of amount 
balance this month

check
select transaction in date 

expense

'''
