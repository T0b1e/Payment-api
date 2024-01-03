import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import requests

cred = credentials.Certificate('credentials.json')

app = firebase_admin.initialize_app(cred, {
    'databaseURL': '...'
})

transactions_ref = db.reference("transactions")

def on_snapshot(event):

    raw_data = event.data

    print(raw_data)

    if 'action' in raw_data and 'add_on' in raw_data and 'types' in raw_data and 'wallet' in raw_data and 'wallet_after_balance' in raw_data:
        
        payload = {
            'action': raw_data['action'],
            'wallet_id': raw_data['wallet'], 
            'wallet_after_balance': raw_data['wallet_after_balance'],
            'types': raw_data['types'],
            'rawAmount': raw_data['add_on']
        }
        
        script_url = "..."
    
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
