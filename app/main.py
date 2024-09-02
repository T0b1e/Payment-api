from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks

import httpx
import requests

import firebase_admin
from firebase_admin import db, credentials

from datetime import datetime, timedelta
from typing import Optional
import urllib.parse
import json
import dotenv
import os

# from fastapi.security import OAuth2PasswordBearer
# from fastapi.logger import logger
# from pydantic import HttpUrl
# from typing import ClassVar
# from pydantic_settings import BaseSettings
# from pyngrok import ngrok
# import uvicorn

# Loaded keys
dotenv.load_dotenv('./keys.env')
api_key = os.getenv('API_KEY')
scripts_url = os.getenv('APPSCRIPTS_URL')
db_url = os.getenv('FIREBASE_URL')

app = FastAPI()

current_datetime_utc = datetime.utcnow()
current_datetime = current_datetime_utc + timedelta(hours=7)

date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H:%M:%S')


def load_credentials():
    if 'DYNO' in os.environ:
        credentials_from_env = os.getenv('CREDENTIALS')
        if credentials_from_env:
            return json.loads(credentials_from_env)
        else:
            raise ValueError("Environment variable 'CREDENTIALS' is missing.")
    else:
        cred_file_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
        if os.path.exists(cred_file_path):
            with open(cred_file_path, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"cred.json file not found at {cred_file_path}. Ensure it's present for local development.")

try:
    cred_data = load_credentials()
    cred = credentials.Certificate(cred_data) 
    firebase_admin.initialize_app(cred, {
                                    "databaseURL": db_url
                                    })

except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")


@app.get("/")
async def root():
    return {"message": "It's Working fine"}


def get_wallet_reference(wallet_name):
    return db.reference(f"/wallet_id/{wallet_name}")


def get_transactions_by_date(date):
    transactions_ref = db.reference("/transactions")
    transactions = transactions_ref.child(date).get()

    if transactions:
        return transactions
    else:
        return {}


def get_transactions_reference():
    return db.reference("/transactions")


def from_eng_to_thai(types):
    mapping = {
    "snacks": "ขนม/น้ำดื่ม",
    "sports": "อุปกรณ์การศึกษา/กีฬา",
    "furnitures": "หอพัก/เฟอร์นิเจอร์",
    "clothings": "เครื่องนุ่งห่ม/เครื่องสำอาง",
    "investment": "ลงทุน (เงินส่วนตัว)" 
    }

    return mapping.get(types, types)


async def push_data_to_google_sheets(transaction_data):
    params = {
        "action": transaction_data['action'],

        "origin_wallet_id": transaction_data.get('wallet', 0),
        "origin_wallet_value": transaction_data.get('wallet_after_balance', 0),

        "destination_wallet_id": transaction_data.get('destination_wallet', ''),
        "destination_wallet_value": transaction_data.get('destination_wallet_value', 0),

        "types": transaction_data['types'],
        "rawAmount": transaction_data.get('add_on', 0),
        "descriptions": transaction_data['descriptions']
    }

    print(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(scripts_url, params=params, follow_redirects=True)
        if response.status_code == 200:
            print("Success! Response:", response.json())
        else:
            print(f"Error! Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")


# Check specify Wallet
@app.get("/api/v5/check/wallet-balance/{wallet_name}")
async def wallet_balance(
    wallet_name: str,
    token: str = Query(..., description="API Key")
):
    if token and token in api_key:
        value = db.reference(f"/wallet_id/{wallet_name}").get()
        
        if value:
            # call to push data into googlesheet 
            return {"date": date_str, "value": round(value, 2)}
        
        raise HTTPException(status_code=404, detail="No value available yet")
    raise HTTPException(status_code=401, detail="Invalid API key")


# Check all Wallet
@app.get("/api/v5/check/wallet-balance")
async def all_wallet_balances(
    token: str = Query(..., description="API Key")
):  

    if token and token in api_key:
 
        value = db.reference("/wallet_id").get()
        rounded_value = {k: round(v, 2) for k, v in value.items()}
        if value:
            return {"date": date_str, "value": rounded_value, "sum": str(round(sum(value.values()), 2)) + " Baht"}
        else:
            raise HTTPException(status_code=404, detail="No value available yet")
    else:
        print("Invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/api/v5/check/transaction/{date}")
async def transactions_by_date(
    date: str,
    token: str = Query(..., description="API Key")

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
    money: str, 
    types: str, 
    background_tasks: BackgroundTasks,
    token: str = Query(..., description="API Key"),
    description: Optional[str] = None
):
    money = float(money)

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
            'add_on': 0, 
            'descriptions': description
        }

        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        ls = []

        if date_entry is not None: # date exits

            for transaction_id, transaction in date_entry.items():
            
                if transaction['action'] == 'income' and transaction['types'] == types:
                    
                    ls.append(float(transaction['amount']))

            transaction_data['add_on'] = sum(ls) + money
            transaction_data['wallet_after_balance'] = new_wallet_value
            transactions_ref.child(date_str).push(transaction_data)

            background_tasks.add_task(push_data_to_google_sheets, transaction_data)

            return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": sum(ls) + money}}
        
        transaction_data['add_on'] = money
        transaction_data['wallet_after_balance'] = new_wallet_value
        transactions_ref.child(date_str).push(transaction_data)

        background_tasks.add_task(push_data_to_google_sheets, transaction_data)
            
        return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": money}}
    
    raise HTTPException(status_code=401, detail="Invalid API keys")


@app.post("/api/v5/expense/{types}")
async def expense(
    wallet_name: str,
    money: str,
    types: str,
    background_tasks: BackgroundTasks,
    token: str = Query(..., description="API Key"),
    description: Optional[str] = None
):
    money = float(money)
    types_in_thai = from_eng_to_thai(types)

    ls = []

    if token in api_key:

        wallet_ref = get_wallet_reference(wallet_name)

        current_wallet_value = wallet_ref.get()
        new_wallet_value = current_wallet_value - money
        wallet_ref.set(new_wallet_value)
        
        transaction_data = {
            'timestamp': time_str,
            'action': "expense",
            'origin_wallet': wallet_name,
            'wallet_after_balance': new_wallet_value,
            'types': types_in_thai,
            'amount': money,
            'add_on': 0, 
            'descriptions': description
        }

        transactions_ref = db.reference('/transactions')

        date_entry = transactions_ref.child(date_str).get()

        ls = []

        if date_entry is not None: # date exits

            for transaction_id, transaction in date_entry.items():

                if transaction['action'] == 'expense' and transaction['types'] == types_in_thai:

                    ls.append(float(transaction['amount']))

            transaction_data['add_on'] = sum(ls) + money
            transaction_data['wallet_after_balance'] = new_wallet_value
            transactions_ref.child(date_str).push(transaction_data)

            transaction_data["types"] = types # Change Lang to pushing into google sheet api 

            background_tasks.add_task(push_data_to_google_sheets, transaction_data)

            return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": sum(ls) + money}}
            
        transaction_data['add_on'] = money
        transaction_data['wallet_after_balance'] = new_wallet_value
        transactions_ref.child(date_str).push(transaction_data)

        transaction_data["types"] = types # Change Lang to pushing into google sheet api 

        background_tasks.add_task(push_data_to_google_sheets, transaction_data)
            
        return {"date": date_str, "value": {"wallet balance": new_wallet_value, "amount": money, "add on": money}}

    raise HTTPException(status_code=401, detail="Invalid API keys")


@app.post("/api/v5/transfer")
async def transfer_funds(
    origin_wallet_name: str,
    destination_wallet_name: str,
    money: float,
    background_tasks: BackgroundTasks,
    token: str = Query(..., description="API Key"),
    description: Optional[str] = None,
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
            'action': "transfer",
            'types': "transfer",
    
            'wallet': origin_wallet_name,
            'wallet_after_balance': new_origin_balance,
            'origin_wallet': origin_wallet_name,
            'origin_wallet_value': new_origin_balance,

            'destination_wallet': destination_wallet_name,
            'destination_wallet_value': new_destination_balance,
            
            'amount': money,
            'add_on': 0,
            'descriptions': description 
        }

        transactions_ref = db.reference('/transactions')
        transactions_ref.child(date_str).push(origin_transaction_data)

        background_tasks.add_task(push_data_to_google_sheets, origin_transaction_data)

        return {"date": date_str, "value": {"origin wallet balance": new_origin_balance, 
                                            "destination wallet balance": new_destination_balance, 
                                            "amount": money}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/api/v1/modify") TODO

# uvicorn main:app --reload --host 0.0.0.0 --port 8000
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


