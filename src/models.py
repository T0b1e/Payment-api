from sqlalchemy import Column, Integer, String, Float
from .database import Base

class User(Base):
    __tablename__ = "narongkorn"

    id      =               Column(Integer, primary_key=True, index=True)
    name    =               Column(String, unique=True)
    deposit =               Column(Float)
    cash    =               Column(Float)

class Categories(Base):
    __tablename__ = "categories"

    id      =               Column(Integer, primary_key=True, index=True)
    name    =               Column(String, unique=True)
    type    =               Column(String)
    
class Transactions(Base):
    __tablename__ = "transactions"

    id      =               Column(Integer, primary_key=True, index=True)
    date    =               Column(String)
    amount   =              Column(Float)
    category   =            Column(String)
    description   =         Column(String)

class Record(Base):
    __tablename__ = "record"

    id      =               Column(Integer, primary_key=True, index=True)
    date    =               Column(String)
    time   =                Column(Float)
    amount   =              Column(Float)
    category   =            Column(String)
    deposit  =              Column(Float)
    cash   =                Column(Float)
    description   =         Column(String)