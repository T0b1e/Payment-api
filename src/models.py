from sqlalchemy import Column, Integer, String, Float, Date, Time, MetaData
from src.database import Base

from datetime import datetime

current = datetime.now()
currentDate = current.date().strftime('%Y-%m-%d')
currentTime = current.time().strftime('%H:%M:%S')

metadata = MetaData()

class Main(Base):
    __tablename__ = "wallet"

    id =        Column(Integer, primary_key=True, index=True)
    name =      Column(String, unique=True, index=True)
    wallet_id = Column(Integer)
    deposit =   Column(Float)
    cash =      Column(Float)


class TranscationsTable(Base):
    __tablename__ = "log"

    id =        Column(Integer, primary_key=True, index=True)
    date =      Column(Date)  # aka timestamp
    time =      Column(Time)  
    category =  Column(String) # aka type
    amount =    Column(Float)
    cash =      Column(Float)
    deposit =   Column(Float)
    description = Column(String)


class IncomeTable(Base):
    __tablename__ = "income"

    id =        Column(Integer, primary_key=True, index=True)
    date =      Column(Date) 
    time =      Column(Time)  
    category =  Column(String)
    wallet_id = Column(Integer)
    amount =    Column(Float)
    tag_id =    Column(Integer)
    description = Column(String)


class ExpenseTable(Base):
    __tablename__ = "expense"

    id =        Column(Integer, primary_key=True, index=True)
    date =      Column(Date)  
    time =      Column(Time)  
    category =  Column(String)
    wallet_id = Column(Integer)
    amount =    Column(Float)
    tag_id =    Column(Integer)
    description = Column(String)



# Note pydantic is only using for focus on data type or string (In this case is not nessesary to using it now but in the future we will talk about that later)
"""
class TransactionBase(BaseModel):
    id:        Union[int, None] = None
    date:      Union[str, None] = None
    time:      Union[str, None] = None
    category:  str
    amount:    float
    cash:      Union[float, None] = None
    deposit:   Union[float, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
"""