from sqlalchemy import Column, Integer, String, Float, Date, Time
from src.database import Base

class Main(Base):
    __tablename__ = "narongkorn"

    id =        Column(Integer, primary_key=True, index=True)
    name =      Column(String, unique=True, index=True)
    deposit =   Column(Float)
    cash =      Column(Float)

class Transcations(Base):
    __tablename__ = "transactions"

    id =        Column(Integer, primary_key=True, index=True)
    date =      Column(Date, default=True)
    time =      Column(Time, default=True)
    category =  Column(String)
    amount =    Column(Float)
    cash =      Column(Float)
    deposit =   Column(Float)
    description = Column(String)

