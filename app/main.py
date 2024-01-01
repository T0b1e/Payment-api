from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn

import firebase_admin
from firebase_admin import db, credentials

from datetime import datetime, timedelta

from typing import Union, Optional

import dotenv
import os

dotenv.load_dotenv('...')

api_key = os.getenv('API_KEY')

app = FastAPI()

current_datetime_utc = datetime.utcnow()

current_datetime = current_datetime_utc + timedelta(hours=7)

date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H:%M:%S')

cred = credentials.Certificate("...")
firebase_admin.initialize_app(cred, {
                                    "databaseURL": "..."
                                    })

@app.get("/")
async def root():
    return {"message": "It's Working fine"}


def get_wallet_reference(wallet_name):
    return db.reference(f"/wallet_id/{wallet_name}")


def get_all_wallet_balances():
    wallet_ref = db.reference("/wallet_id")
    wallets = wallet_ref.get()

    if wallets:
        return wallets
    else:
        return {}


def get_transactions_by_date(date):
    transactions_ref = db.reference("/transactions")
    transactions = transactions_ref.child(date).get()

    if transactions:
        return transactions
    else:
        return {}


def get_transactions_reference():
    return db.reference("/transactions")


@app.get("/api/v5/check/wallet-balance")
async def wallet_balance(
    wallet_name: str,
    token: str
):
    if token and token in api_key:
        wallet_ref = get_wallet_reference(wallet_name)
        value = wallet_ref.get()

        if value:
            return {"date": f'2023-10-01 --> {date_str}', "value": value}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/api/v5/check/wallet-balance/all")
async def all_wallet_balances(
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:

        value = get_all_wallet_balances()

        if value:
            return {"date": f'2023-01-01 --> {date_str}', "value": value, "sum": str(round(sum(value.values()), 2)) + " Baht"}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/api/v5/check/transaction/{date}")
async def transactions_by_date(
    date: str,
    token: str
):
    if token and token in api_key:

        transactions = get_transactions_by_date(date)

        if not transactions:
            raise HTTPException(status_code=404, detail="Error :(")
        
        total_amount = sum(transaction.get("amount", 0) for transaction in transactions.values())

        return {
            "date": date,
            "transactions": transactions,
            "total_amount": total_amount,
        }
    
    raise HTTPException(status_code=401, detail="Invalid API key")


@app.post("/api/v5/income/{types}")
async def income(
    wallet_name: str,
    money: float, 
    types: str, 
    token: str,
    description: Optional[str] = None
):
    if token in api_key:
        wallet_ref = get_wallet_reference(wallet_name)

        current_wallet_value = wallet_ref.get()
        new_wallet_value = current_wallet_value + money
        wallet_ref.set(new_wallet_value)

        transaction_data = {
        'timestamp': time_str,
        'action': "income", 
        'wallet': wallet_name, 
        'wallet_after_balance': new_wallet_value,
        'types': types, 
        'amount': money,
        'add_on': 0,  # reduce queary method
        'description': description 
        }

        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        ls = []

        if date_entry is not None: # date exits

            for transaction_id, transaction in date_entry.items():

                if transaction['action'] == 'expense' and transaction['types'] == types:

                    ls.append(float(transaction['amount']))

            transaction_data['add_on'] = sum(ls) + money
            transaction_data['wallet_after_balance'] = new_wallet_value
            transactions_ref.child(date_str).push(transaction_data)

            return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": sum(ls) + money}}
            
        transaction_data['add_on'] = money
        transaction_data['wallet_after_balance'] = new_wallet_value
        transactions_ref.child(date_str).push(transaction_data)
            
        return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": money}}
    
    raise HTTPException(status_code=401, detail="Invalid API keys")


@app.post("/api/v5/expense/{types}")
async def expense(
    wallet_name: str,
    money: float,
    types: str,
    token: str,
    description: Optional[str] = None
):
    ls = []

    if token in api_key:

        wallet_ref = get_wallet_reference(wallet_name)

        current_wallet_value = wallet_ref.get()
        new_wallet_value = current_wallet_value - money
        wallet_ref.set(new_wallet_value)

        transaction_data = {
            'timestamp': time_str,
            'action': "expense",
            'wallet': wallet_name,
            'wallet_after_balance': new_wallet_value,
            'types': types,
            'amount': money,
            'add_on': 0, 
            'description': description
        }

        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        ls = []

        if date_entry is not None: # date exits

            for transaction_id, transaction in date_entry.items():

                if transaction['action'] == 'expense' and transaction['types'] == types:

                    ls.append(float(transaction['amount']))

            transaction_data['add_on'] = sum(ls) + money
            transaction_data['wallet_after_balance'] = new_wallet_value
            transactions_ref.child(date_str).push(transaction_data)

            return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": sum(ls) + money}}
            
                
        transaction_data['add_on'] = money
        transaction_data['wallet_after_balance'] = new_wallet_value
        transactions_ref.child(date_str).push(transaction_data)
            
        return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": money}}

    raise HTTPException(status_code=401, detail="Invalid API keys")


@app.post("/api/v5/transfer")
async def transfer_funds(
    origin_wallet_name: str,
    destination_wallet_name: str,
    money: float,
    token: str = Query(default=None, max_length=50),
    description: str = None,
):
    if token not in api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    origin_wallet_ref = get_wallet_reference(origin_wallet_name)
    destination_wallet_ref = get_wallet_reference(destination_wallet_name)

    origin_balance = float(origin_wallet_ref.get())
    destination_balance = float(destination_wallet_ref.get())

    if origin_balance < money:
        raise HTTPException(status_code=400, detail="Insufficient funds in the origin wallet")

    new_origin_balance = origin_balance - money
    new_destination_balance = destination_balance + money

    origin_wallet_ref.set(new_origin_balance)
    destination_wallet_ref.set(new_destination_balance)

    try:

        origin_transaction_data = {
            'timestamp': time_str,
            'action': "expense",
            'wallet': origin_wallet_name,
            'wallet_after_balance': new_origin_balance,
            'types': "transfer",
            'amount': money,
            'description': description 
        }

        destination_transaction_data = {
            'timestamp': time_str,
            'action': "income",
            'wallet': destination_wallet_name,
            'wallet_after_balance': new_destination_balance,
            'types': "transfer",
            'amount': money,
            'description': description 
        }

        transactions_ref = db.reference('/transactions')
        transactions_ref.child(date_str).push(origin_transaction_data)
        transactions_ref.child(date_str).push(destination_transaction_data)

        return {"date": date_str, "value": {"origin wallet balance": new_origin_balance, 
                                            "destination wallet balance": new_destination_balance, 
                                            "amount": money}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @app.post("/api/v1/modify") TODO



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


