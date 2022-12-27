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

@app.post("/expense/{types}/{money}")
async def expense(types: str, money: float, description: Union[str, None] = None):
    return {"date": "2022-12-27", #TODO
            "value": PaymentMethod().expense(amount=money, types=types, description=description)}

@app.post("/income/{types}/{money}")
async def income(types: str, money: float, description: Union[str, None] = None):
    return {"date": "2022-12-27", #TODO
            "value": PaymentMethod().income(amount=money, types=types, description=description)}

@app.post("/transactions/{types}/{money}")
async def transactions(types: str, money: float, description: Union[str, None] = None):
    return {"date": "2022-12-27", #TODO
            "value": PaymentMethod().transactions(amount=money, types=types, description=description)}


'''
checks
sum of amount 
balance this month

check
select transaction in date 

expense

'''
