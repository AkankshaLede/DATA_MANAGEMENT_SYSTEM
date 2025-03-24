import uvicorn
from fastapi import FastAPI, requests
from contextlib import asynccontextmanager
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from psycopg.rows import dict_row
import logging
from db_helper import DBConnectionPool
from model import Employee
from unittest import TestCase
# import unittest
# import requests



logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(obj: FastAPI):
    obj.async_pool = DBConnectionPool()
    await obj.async_pool.psyco_async_pool.open()
    yield
    await obj.async_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get(
    '/employee_data/{emp_id}',
    status_code = status.HTTP_200_OK,
    name = "Get employee data by employee id"
)

async def get_employee_data(
    request: Request,
    emp_id : int
):
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory = dict_row) as cur:
                await cur.execute("""
                    SELECT 
                    emp_id,
                    fname,
                    lname,
                    email,
                    dept,
                    salary,
                    hire_date :: text
                    FROM public.employee where emp_id = %s
                    """,(emp_id,))
                
                results = await cur.fetchone()
                if results:
                    return JSONResponse({
                        "status" : True,
                        "message" : "successful",
                        "data" : results
                    })
                else:
                    return JSONResponse({
                        "status" : False,
                        "message" : "data not found"
                    })
                
    except Exception as e:
        logger.error("Error fetching : %s",str(e))
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
@app.post(
    '/insertemployee',
    status_code = status.HTTP_201_CREATED,
    name = "Insert data into employee"
)

async def insert_employee_data(
    request:Request,
    employee : Employee
):
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory = dict_row) as cur:
                await cur.execute("""
                INSERT INTO public.employee
                (emp_id,fname,lname,email,dept,salary,hire_date)
                VALUES(%s,%s,%s,%s,%s,%s,%s) returning *
                """,
                (employee.emp_id,employee.fname,employee.lname,employee.email,employee.dept,employee.salary,employee.hire_date,)
                )
                emp_id = await cur.fetchone()
                return {"status": True, "message": "Data added successfully", "id": emp_id}
    except Exception as e:
        logger.error("Error inserting data: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# URL = "http://127.0.0.1:8000"

# class TestAPI(TestCase):
#     def test_get_items(self):
#         emp_id = 4
#         url = f"{URL}/employee_data/{emp_id}"
#         a = requests.get(url)
#         self.assertEqual(a.status_code, 200)

#     def test_get_items_(self):
#         emp_id = "yeruk"
#         url = f"{URL}/employee_data/{emp_id}"
#         a = requests.get(url)
#         self.assertEqual(a.status_code, 200 ,msg = "please enter proper employee_id in integer" )

#     def test_post_items(self):
#         url = f"{URL}/insertemployee"
#         data = {
#             "emp_id": 7,
#             "fname": "Akanksha",
#             "lname": "Lede",
#             "email": "akanksha.lede@moschip.com",
#             "dept": "backend",
#             "salary": 29500,
#             "hire_date": "2024-08-05"
#         }
#         b = requests.post(url, json = data)
#         self.assertEqual(b.status_code, 201)

#     def test_post_items(self):
#         url = f"{URL}/insertemployee"
#         data = {
#             "emp_id" : 5,
#             "fname" : "akshu",
#             "lname" : "lede",
#             "email" : "akshu@gmail.com",
#             "dept" : "frontend",

#         }
#         c = requests.post(url, json = data)
#         self.assertEqual(c.status_code, 422, msg = "Invalid data,field proper data")



if __name__ == "__main__":
    # unittest.main()
    uvicorn.run("main:app", host="195.168.1.125", port=8000, reload= True)