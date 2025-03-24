from pydantic import BaseModel
from datetime import date

class Employee(BaseModel):
    emp_id : int
    fname : str
    lname : str
    email : str
    dept : str
    salary : int
    hire_date : date


