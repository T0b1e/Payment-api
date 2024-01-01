import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import requests

cred = credentials.Certificate('credentials.json')

app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ledger-c71bc-default-rtdb.firebaseio.com/'
})

transactions_ref = db.reference("transactions")

def on_snapshot(event):

    raw_data = event.data

    if 'action' in raw_data and 'add_on' in raw_data and 'types' in raw_data and 'wallet' in raw_data and 'wallet_after_balance' in raw_data:

        payload = {
            'action': raw_data['action'],
            'rawAmount': raw_data['add_on'],
            'types': raw_data['types'],
            'wallet_id': raw_data['wallet'], 
            'wallet_after_balance': raw_data['wallet_after_balance'] 
        }

        print(payload)
        
        script_url = "https://script.google.com/macros/s/AKfycbyq8p3X529rM5FusrKmLwDUnEUoxRgnMfZcKP5dGRcnESHQupJtStkXkuPv6I3qluaL/exec"
    
        response = requests.get(script_url, params = payload)
        
        if response.status_code == 200:

            print("Success! Response:", response.json())

        else:
            print("Error! Status Code:", response.status_code)
            print("Response Text:", response.text)

    else:

        pass
       
    
transactions_ref.listen(on_snapshot)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    firebase_admin.delete_app(app)
