import mysql.connector
from readExcel import rawData

db = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='na592600',
    database='payments'
)

# , bank_balance, balance, salary, income, other_income, breakfast, lunch, dinner, water_snack, convenience_store, travelling, education, entertain, crafting, investment, other_expenses
cursor = db.cursor()

month = 'august'

def createTable():

  sql = f'''
  CREATE TABLE december
  (
    date INT NOT NULL PRIMARY KEY,
    bank_balance FLOAT NOT NULL,
    balance FLOAT NOT NULL,
    salary FLOAT DEFAULT '0',
    income FLOAT DEFAULT '0',
    other_income FLOAT DEFAULT '0',
    breakfast FLOAT DEFAULT '0',
    lunch FLOAT DEFAULT '0',
    dinner FLOAT DEFAULT '0',
    water_snack FLOAT DEFAULT '0',
    convenience_store FLOAT DEFAULT '0',
    travelling FLOAT DEFAULT '0',
    education FLOAT DEFAULT '0',
    entertain FLOAT DEFAULT '0',
    crafting FLOAT DEFAULT '0',
    investment FLOAT DEFAULT '0',
    other_expenses FLOAT DEFAULT '0'
  )
  '''  

  cursor.execute(sql)
  db.commit()

  db.close()
  cursor.close()

  return 0


def insertData():

  sql = f'''INSERT INTO november (date, bank_balance, balance, salary, income, other_income, breakfast, lunch, dinner, 
  water_snack, convenience_store, travelling, education, entertain, crafting, investment, other_expenses) 
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

  value = rawData()

  cursor.executemany(sql, value)
  db.commit()

  db.close()
  cursor.close()

  return 0

def updateTable():

  sql = f'''UPDATE october SET date = %s, bank_balance, balance, salary, income, other_income, breakfast, lunch, dinner, 
  water_snack, convenience_store, travelling, education, entertain, crafting, investment, other_expenses) 
  VALUES (, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

  value = rawData()

  cursor.executemany(sql, value)
  db.commit()

  db.close()
  cursor.close()

  return 0

# createTable()
insertData()

