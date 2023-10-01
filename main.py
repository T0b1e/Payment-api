from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from sqlalchemy.orm import Session

from src.crud import addExpense, addIncome, transfer_between_wallets
from src.checkMethod import checkWalletBalance, checkAllWalletBalance, checkTransactions

from src.database import SessionLocal, engine
import src.models as models
from src.sheet.updateSheet import sending_package

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


def check_all(db: Session):
    # Implement your checkAll logic here
    pass

@app.get("/api/v2/status")
async def check_balance(
    db: Session = Depends(get_db),
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:
        value = check_all(db)
        if value:
            return {"date": f'2023-01-01 --> {presentDate}', "value": value}
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=404, detail="Invalid API key")


@app.get("/api/v2/check/wallet-balance") # Specify wallet
async def wallet_balance(
    wallet_name: str,
    db: Session = Depends(get_db),
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:
        value = checkWalletBalance(db=db, wallet_name=wallet_name)

        if value:
            return {"date": f'2023-10-01 --> {presentDate}', "value": value}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=404, detail="Invalid API key")


@app.get("/api/v2/check/wallet-balance/all")  # none param
async def all_wallet_balances(
    db: Session = Depends(get_db),
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:
        value = checkAllWalletBalance(db)
        if value:
            return {"date": f'2023-01-01 --> {presentDate}', "value": value}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=404, detail="Invalid API key")


@app.get("/api/v2/check/transaction/{date}")  # Specify date
async def transactions_by_date(
    date: str,
    db: Session = Depends(get_db),
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:
        transactions = checkTransactions(db=db, date=date)

        if not transactions:
            raise HTTPException(status_code=404, detail="Error :(")
        
        total_amount = sum(transactions.values())

        return {
            "date": date,
            "transactions": transactions,
            "total_amount": total_amount,
        }
    
    raise HTTPException(status_code=404, detail="Invalid API key")


@app.post("/api/v2/income/{types}")
async def income(
    wallet_name: str,
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
):
    if token in api_key:
        value = await addIncome(db=db, types=types, wallet_name=wallet_name, amount=money, description=description)

        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        try:

            result = await sending_package(
                action="income",
                wallet_id=wallet_name,
                types=types,
                amount=value.amount,
            )

            if result.get("status") == "success":
                return {"date": presentDate, "value": value}
            else:
                raise HTTPException(status_code=500, detail="Sending package error")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=404, detail="Invalid API keys")


@app.post("/api/v2/expense/{types}")
async def expense(
    wallet_name: str,
    money: float, 
    types: str, 
    token: Union[str, None] = Query(default=Required, max_length=50),
    description: Union[str, None] = None, 
    db: Session = Depends(get_db)
    ):

    if token in api_key:
        value = await addExpense(db=db, types=types, wallet_name=wallet_name , amount=money, description=description)

        if not value:
            raise HTTPException(status_code=404, detail="Error :(")

        try:

            result = await sending_package(
                action = "expense",
                wallet_id = wallet_name,
                types = types,
                amount = value.amount,
            )

            if result.get("status") == "success":
                return {"date": presentDate, "value": value}
            else:
                raise HTTPException(status_code=500, detail="Sending package error")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=404, detail="Invalid API keys")


@app.post("/api/v2/transfer")
async def transfer_funds(
    origin_wallet_name: str,
    destination_wallet_name: str,
    money: float,
    token: str = Query(default=None, max_length=50),
    description: str = None,
    db: Session = Depends(get_db)
):
    if token in api_key:
        transfer_result = await transfer_between_wallets( 
            db=db, 
            origin_wallet_name=origin_wallet_name, 
            destination_wallet_name=destination_wallet_name, 
            amount=money, 
            description=description 
        )

        if not transfer_result:
            raise HTTPException(status_code=404, detail="Error :(")

        try:

            result = await sending_package(
                action="transfer",
                wallet_id=origin_wallet_name,
                types="transfer",
                origin_wallet_value=transfer_result.origin_wallet_value,
                destination_wallet_id=destination_wallet_name,
                destination_wallet_value=transfer_result.destination_wallet_value,
                amount=money,
            )
        
            if result.get("status") == "success":
                return {"date": presentDate, "value": transfer_result}
            else:
                raise HTTPException(status_code=500, detail="Sending package error")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=404, detail="Invalid API keys")


@app.post("/api/v1/modify")
async def transfer_funds(
    origin_wallet_name: str,
    destination_wallet_name: str,
    money: float,
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
        amount =  money,
        description =  description
    )

    if transfer_result: 

        result = sending_package(
            action = "transfer",
            wallet_id = origin_wallet_name,
            types = "transfer",
            origin_wallet_value = transfer_result.origin_wallet_value,
            destination_wallet_id = destination_wallet_name,
            destination_wallet_value = transfer_result.destination_wallet_value,
            amount = money,
        )
        
        return {"message": "Transfer successful", "transaction_id": transfer_result.id}
    else:
        raise HTTPException(status_code=400, detail="Transfer failed")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


