from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import uvicorn

import firebase_admin
from firebase_admin import db, credentials

from datetime import datetime, timedelta

from typing import Union, Optional

import dotenv
import os

dotenv.load_dotenv('../keys.env')

api_key = os.getenv('API_KEY')

app = FastAPI()

current_datetime_utc = datetime.utcnow()

current_datetime = current_datetime_utc + timedelta(hours=7)

date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H:%M:%S')

cred = credentials.Certificate("../credentials.json")
firebase_admin.initialize_app(cred, {
                                    "databaseURL": "https://ledger-c71bc-default-rtdb.firebaseio.com/"
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


@app.get("/api/v2/check/wallet-balance")
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


@app.get("/api/v2/check/wallet-balance/all")
async def all_wallet_balances(
    token: Union[str, None] = Query(default=None, max_length=50)
):
    if token and token in api_key:

        value = get_all_wallet_balances()

        if value:
            return {"date": f'2023-01-01 --> {date_str}', "value": value, "sum": str(round(sum(value.values()), 2)) + " Baht"}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/api/v2/check/transaction/{date}")
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


@app.post("/api/v2/income/{types}")
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
        'description': description 
        }

        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        if date_entry is None:
            transactions_ref.child(date_str).set({})

        transactions_ref.child(date_str).push(transaction_data)

        return {"date": date_str, "value": {"wallet balance": new_wallet_value, 
                                               "amount": money}}
    
    raise HTTPException(status_code=401, detail="Invalid API keys")


@app.post("/api/v2/expense/{types}")
async def expense(
    wallet_name: str,
    money: float, 
    types: str,
    token: str,
    description: Optional[str] = None
):
    if token in api_key:
        wallet_ref = get_wallet_reference(wallet_name)

        current_wallet_value = wallet_ref.get()
        new_wallet_value = current_wallet_value - money
        wallet_ref.set(new_wallet_value)

        transaction_data = {
            'timestamp': time_str,
            'action': "expense",  # Updated to "expense"
            'wallet': wallet_name, 
            'wallet_after_balance': new_wallet_value,  # Updated to use new_balance
            'types': types, 
            'amount': money,
            'description': description 
        }
        
        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        if date_entry is None:
            transactions_ref.child(date_str).set({})

        transactions_ref.child(date_str).push(transaction_data)
        
        return {"date": date_str, "value": {"wallet balance": new_wallet_value, 
                                               "amount": money}}
    
    raise HTTPException(status_code=401, detail="Invalid API keys")



@app.post("/api/v2/transfer")
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

"""
@app.post("/api/v1/modify")
async def modify_transaction(
    date:               str = Query(..., description="Date of the transaction (format: YYYY-MM-DD)"),
    transaction_id:     str = Query(..., description="ID of the transaction to modify"),
    new_description:    str = Query(None, description="New description for the transaction"),
    new_amount:         float = Query(None, description="New amount for the transaction"),
    new_wallet_balance: float = Query(None, description="New wallet balance"),
    token:              str = Query(default=None, max_length=50),
):
    if token and token not in api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        transactions_ref = db.reference('/transactions')
        transaction_ref = transactions_ref.child(date).child(transaction_id)

        existing_transaction = transaction_ref.get()

        if existing_transaction:
            # Update the transaction based on provided parameters
            if new_description:
                existing_transaction['description'] = new_description

            if new_amount is not None:
                existing_transaction['amount'] = new_amount

            # Update the wallet balance if specified
            if new_wallet_balance is not None:
                existing_transaction['wallet_after_balance'] = new_wallet_balance

            # Update the transaction in the database
            transaction_ref.update(existing_transaction)

            # Return the modified transaction
            return {"message": "Transaction modified successfully", "transaction": existing_transaction}
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


