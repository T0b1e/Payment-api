from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import sum as sums
from sqlalchemy.exc import IntegrityError
from src.models import Main, TransactionsTable, IncomeTable, ExpenseTable, TransferTable
from datetime import datetime, date


async def addIncome(db: Session, wallet_name: str, amount: float, types: str, description: str): #income

    main_info = db.query(Main.name, Main.deposit).filter(Main.name == wallet_name).first()
    if main_info:
        wallet_name, deposit = main_info

        if deposit >= amount:
            db.query(Main).filter(Main.name == wallet_name).update({Main.deposit: Main.deposit + amount})  # update wallet table
            updated_deposit = db.query(Main.deposit).filter(Main.name == wallet_name).first()[0]

            data = IncomeTable( # update income table
                date = date.today(),
                time = datetime.now().time(),
                category = types,
                wallet_id = wallet_name,
                amount = amount, # After adding value
                description = description
            )

            log = TransactionsTable(
                date = date.today(),
                time = datetime.now().time(),
                action = 'income',
                types = types,
                amount = amount,
                # cash = cash,
                # deposit = updated_deposit, 
                origin_wallet_name = wallet_name,
                origin_wallet_value = updated_deposit,
                # destination_wallet_name =     
                # destination_wallet_value =    
                # tag_id = 
                description = description
            )

            db.add(data)
            db.add(log)
            db.commit()
            db.refresh(data)

            return data
        else:
            return None

    return None

async def addExpense(db: Session, wallet_name: str, amount: float, types: str, description: str): #expense 

    main_info = db.query(Main.name, Main.deposit).filter(Main.name == wallet_name).first()

    if main_info:
        wallet_name, deposit = main_info

        if deposit >= amount:
            db.query(Main).filter(Main.name == wallet_name).update({Main.deposit: Main.deposit - amount}) # update wallet table
            updated_deposit = db.query(Main.deposit).filter(Main.name == wallet_name).first()[0]
            db.commit()

            data = ExpenseTable( # update expense table
                date = date.today(),
                time = datetime.now().time(),
                category = types,
                wallet_id = wallet_name,
                amount = amount,
                description = description
            )

            log = TransactionsTable(
                date = date.today(),
                time = datetime.now().time(),
                action = 'expense',
                types = types,
                amount = amount,
                # cash = cash,
                # deposit = updated_deposit, 
                origin_wallet_name = wallet_name,
                origin_wallet_value = updated_deposit,
                # destination_wallet_name =     
                # destination_wallet_value =    
                # tag_id =  
                description = description
            )

            db.add(data)
            db.add(log)
            db.commit()
            db.refresh(data)
            
            return data
        else:
            return None

    return None


async def transfer_between_wallets(db: Session, origin_wallet_name: str, destination_wallet_name: str, amount: float, description: str):
    
        origin_wallet = db.query(Main.deposit).filter(Main.name == origin_wallet_name).first()
        destination_wallet = db.query(Main.deposit).filter(Main.name == destination_wallet_name).first()

        if origin_wallet and destination_wallet:
            origin_wallet_value = origin_wallet[0]  
            destination_wallet_value = destination_wallet[0]  

            if origin_wallet_value >= amount:
                updated_origin_value = origin_wallet_value - amount
                updated_destination_value = destination_wallet_value + amount
                try:
                        # Update wallet values
                        db.query(Main).filter(Main.name == origin_wallet_name).update({Main.deposit: updated_origin_value})
                        db.query(Main).filter(Main.name == destination_wallet_name).update({Main.deposit: updated_destination_value})

                        # Rest of your code

                        db.commit()

                        data = TransferTable(
                            date=date.today(),
                            time=datetime.now().time(),
                            origin_wallet_name=origin_wallet_name,
                            origin_wallet_value=updated_origin_value,
                            destination_wallet_name=destination_wallet_name,
                            destination_wallet_value=updated_destination_value,
                            description=description
                        )

                        log = TransactionsTable(
                            date=date.today(),
                            time=datetime.now().time(),
                            action='transfer',
                            types='transfer',
                            amount=amount,
                            origin_wallet_name=origin_wallet_name,
                            origin_wallet_value=updated_origin_value,
                            destination_wallet_name=destination_wallet_name,
                            destination_wallet_value=updated_destination_value,
                            description=description
                        )

                        db.add(data)
                        db.add(log)
                        db.commit()
                        db.refresh(data)

                        return data
                
                except IntegrityError:
                    db.rollback()  

        return None 


# TODO
"""
def modify(db: Session, date: int, wallet_name: str, amount: float, types: str, description: str):

    main_info = db.query(Main.name, Main.deposit).filter(Main.name == wallet_name).first()

    if main_info:
        wallet_name, deposit = main_info

        if deposit >= amount:
            db.query(Main).filter(Main.name == wallet_name).update({Main.deposit: Main.deposit - amount}) # update wallet table
            db.commit()

            data = ExpenseTable( # update expense table
                date = date.today(),
                time = datetime.now().time(),
                category = types,
                wallet_id = wallet_name,
                amount = Main.deposit - amount,
                description = description
            )

            log = TransactionsTable(
                date = date.today(),
                time = datetime.now().time(),
                action = 'modify',
                types = types,
                amount = amount,
                # cash = cash,
                deposit = updated_deposit, 
                origin_wallet_name = wallet_name,
                # origin_wallet_value = origin_wallet - amount,
                # destination_wallet_name = origin_wallet_name,
                # destination_wallet_value = destination_wallet + amount,   
                # tag_id =  
                description = description
            )

            db.add(data)
            db.commit()
            db.refresh(data)
            
            return data
        else:
            return None

    return None
"""
