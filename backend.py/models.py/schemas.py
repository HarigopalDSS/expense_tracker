from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    n: str
    a: float
    c: str
    d: date
