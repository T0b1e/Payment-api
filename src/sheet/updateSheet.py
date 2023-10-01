import requests
from dotenv import load_dotenv
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_directory, '../Database/keys.env')
load_dotenv(env_path)
url_path = os.getenv('APPS_SCRIPTS_URL')

async def sending_package(action: str, wallet_id: str, types: str, amount: float, 
                          origin_wallet_value= None, destination_wallet_id= None, destination_wallet_value= None, date= None, newType= None):

    # Base payload
    payload = {
        "action": action,
        "wallet_id": wallet_id,
        "types": types,
        "rawAmount": amount,
    }

    # Optional (Transfer)
    if action == "transfer":
        payload["origin"] = origin_wallet_value
        payload["destination_wallet_id"] = destination_wallet_id
        payload["destination"] = destination_wallet_value

    # Optional (Modify)
    if action == "modify":
        payload["date"] = date
        payload["newType"] = newType

    try:
        response = requests.get(url_path, params=payload)
        response.raise_for_status()
        print("Data package to sheet successfully.")
        print("Response:", response.text)
        
        return {"status": "success", "data": response.text}
    except Exception as e:
        # print("Error:", str(e))
        
        return {"status": "error", "message": str(e)}




# Testing Production

if __name__ == "__main__":
    # Test for Income
    income_response = sending_package(
        action="income",
        wallet_id="SCBx",
        types="เงินเดือน",
        amount=100,
    )

    # Test for Expense
    expense_response = sending_package(
        action="expense",
        wallet_id="SCBx",
        types="ข้าวเช้า",
        amount=50,
    )

    # Test for Transfer
    transfer_response = sending_package(
        action="transfer",
        wallet_id="Pocket Bank",
        types="transfer",
        origin_wallet_value=200,
        destination_wallet_id="SCBx",
        destination_wallet_value=300,
        amount=50,
    )

    # Test for Modify
    modify_response = sending_package(
        action="modify",
        wallet_id="SCBx",
        types="เงินเดือน",
        amount=150,
        date="2023-10-15",
        newType="รายได้",
    )

    # Print the responses
    # print("Income Response:", income_response)
    # print("Expense Response:", expense_response)
    # print("Transfer Response:", transfer_response)
    # print("Modify Response:", modify_response)





