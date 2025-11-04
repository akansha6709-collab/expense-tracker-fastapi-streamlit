from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware

from Backend import db_helper

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExpenseIn(BaseModel):
    expense_date: str
    amount: Decimal = Field(gt=0)
    category: str
    notes: Optional[str] = None

class ExpenseOut(ExpenseIn):
    id: int

@app.get("/expenses", response_model=List[ExpenseOut])
def list_expenses(expense_date: Optional[str] = None):
    try:
        rows = db_helper.read(expense_date)
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expenses")
def add_expense(exp: ExpenseIn):
    try:
        db_helper.insert(exp.dict())
        return {"msg": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/expenses/{id}")
def update_expense(id: int, exp: ExpenseIn):
    try:
        db_helper.update(id, exp.dict())
        return {"msg": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/expenses")
def delete_by_date(expense_date: str):
    try:
        db_helper.delete_by_date(expense_date)
        return {"msg": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary")
def summary(start_date: str, end_date: str):
    return db_helper.summary(start_date, end_date)

@app.get("/analytics/categories")
def categories(start_date: str, end_date: str):
    return db_helper.analytics_categories(start_date, end_date)

@app.get("/analytics/category-trend")
def category_trend(category: str, start_date: str, end_date: str):
    return db_helper.analytics_category_trend(category, start_date, end_date)
