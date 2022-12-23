from fastapi import FastAPI

from src.crud import PaymentMethod

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check")
async def checks():
    return {"value": PaymentMethod.checkAll()}

@app.get("/check/{date}")
async def check(date : int):
    return {"date": date,
            "value": PaymentMethod.checkSingle(date=date)}

@app.post("/upload/{date}/{types}/{money}")
async def upload(date: int, types: str, money: float):
    return {"date": date,
            "value": PaymentMethod.upload(date=date, types=types, money=money)}

