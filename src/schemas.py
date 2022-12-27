from pydantic import BaseModel

class DataBase(BaseModel):
    date                : int
    bank_balance        : float
    balance             : float
    salary              : float
    income              : float
    other_income        : float
    breakfast           : float
    lunch               : float
    dinner              : float
    water_snack         : float
    convenience_store   : float
    travelling          : float
    education           : float
    entertain           : float
    crafting            : float
    investment          : float
    other_expenses      : float