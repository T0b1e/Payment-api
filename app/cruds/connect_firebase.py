import firebase_admin
from firebase_admin import db, credentials

EMAIL = "narongkorn.k65@rsu.ac.th"
PASS = "NarongkornAtRSU"

config = {
    "apiKey": "AIzaSyB7IDKjSM1h5ec_-LrSzxQR8zxJzatljx8",
    "authDomain": "ledger-c71bc.firebaseapp.com",
    "databaseURL": "https://ledger-c71bc-default-rtdb.firebaseio.com",
    "projectId": "ledger-c71bc",
    "storageBucket": "ledger-c71bc.appspot.com",
    "messagingSenderId": "583216416032",
    "appId": "1:583216416032:web:3e88bf578f8bda2b3a8345",
    "measurementId": "G-36C3V5G349" 
}

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
                                    "databaseURL": "https://ledger-c71bc-default-rtdb.firebaseio.com/"
                                    })

# Check method
WALLET = "SCB"

def check(wallet : str, all = False):
    if all: # Check All Wallet
        wallet_value = db.reference(f"/wallet_id")
        result = wallet_value.get() # {'BLB': '0', 'BTS Card': 0, 'MRT Card': 0, 'Red Card': 0, 'SCB': 0, 'True Wallet': '0', 'Wallet': 0}
    else: # Specify Wallet
        wallet_value = db.reference(f"/wallet_id/{wallet}")
        result = wallet_value.get() 
    print(result)

# check(wallet=WALLET, all = True)
    
from datetime import datetime, timedelta

def check_transaction(date: str):
    transactions = db.reference("/transactions")
    result = transactions.get()

    # Parse the input date in ISO 8601 format
    input_date = datetime.fromisoformat(date)

    # Check if there are transactions for the given date
    if result and input_date.isoformat() in result:
        print("Transactions for {}: {}".format(date, result[input_date.isoformat()]))
    else:
        # If no transactions for the given date, or date is in the future
        today_date = datetime.now().isoformat()
        if input_date > datetime.now():
            print("No transactions for future date: {}".format(date))
        else:
            print("No transactions for today or past date: {}".format(today_date))

# Example usage:
# check_transaction("2023-12-29")

def income(wallet:str, types:str, amount:float, description:str): 

    wallet_ref = db.reference(f"/wallet_id/{wallet}").get()

    current_balance = float(wallet_ref.get())
    new_balance = current_balance - amount
    wallet_ref.set(new_balance)
    
    db.reference(f"/wallet_id/{wallet}").set(new_balance)

    current_datetime_utc = datetime.utcnow()

    # Add the UTC+7 offset for Thailand time zone
    current_datetime = current_datetime_utc + timedelta(hours=7)

    date_str = current_datetime.strftime('%Y-%m-%d')
    time_str = current_datetime.strftime('%H:%M:%S')
    
    transaction_data = {
        'timestamp': time_str,
        'action': "income", 
        'wallet': wallet, 
        'wallet_after_balance': current_balance, 
        'types': types, 
        'amount': amount,
        'description': description 
    }
    transactions_ref = db.reference('/transactions')
   
    date_exists = transactions_ref.child(date_str).get() is not None

    if date_exists:
        transactions_ref.child(date_str).push(transaction_data)
    else:
        transactions_ref.push(transaction_data)

# income(wallet="SCB", types="ข้าวเช้า", amount=100, description=" ")


def expense(wallet: str, types: str, amount: float, description: str):
    wallet_ref = db.reference(f"/wallet_id/{wallet}")

    current_balance = float(wallet_ref.get())
    new_balance = current_balance - amount
    wallet_ref.set(new_balance)

    current_datetime_utc = datetime.utcnow()

    current_datetime = current_datetime_utc + timedelta(hours=7)

    date_str = current_datetime.strftime('%Y-%m-%d')
    time_str = current_datetime.strftime('%H:%M:%S')

    transaction_data = {
        'timestamp': time_str,
        'action': "expense", 
        'wallet': wallet, 
        'wallet_after_balance': current_balance, 
        'types': types, 
        'amount': amount,
        'description': description 
    }
    transactions_ref = db.reference('/transactions')

    date_exists = transactions_ref.child(date_str).get() is not None

    if date_exists:
        transactions_ref.child(date_str).push(transaction_data)
    else:
        transactions_ref.push(transaction_data)

    print(f"Expense recorded successfully. New wallet balance: {new_balance}")

# Example usage
expense(wallet="SCB", types="Groceries", amount=50, description="Shopping for groceries")
