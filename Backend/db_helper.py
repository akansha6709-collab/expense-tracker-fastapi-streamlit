# Backend/db_helper.py
from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, List, Iterable
import os
from decimal import Decimal

import mysql.connector
try:
    # optional, only if python-dotenv is installed and a .env exists
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

from Backend.logging_setup import setup_logger

logger = setup_logger("db_helper")

import os
def _connect():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST","127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT","3306")),
        user=os.getenv("MYSQL_USER","exp_user"),
        password=os.getenv("MYSQL_PASSWORD",""),
        database=os.getenv("MYSQL_DB","expense_manager"),
    )

# ---- MySQL connection --------------------------------------------------------
def _connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "exp_user"),
        password=os.getenv("DB_PASSWORD", "MyAppPass#123"),
        database=os.getenv("DB_NAME", "expense_manager"),
    )


@contextmanager
def get_db_cursor(commit: bool = False):
    conn = _connect()
    cur = conn.cursor(dictionary=True)
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


# ---- helpers -----------------------------------------------------------------
def _cast_numbers(rows: Iterable[Dict]) -> List[Dict]:
    """Convert Decimal values to float for JSON/Streamlit."""
    out: List[Dict] = []
    for r in rows:
        nr = {}
        for k, v in r.items():
            if isinstance(v, Decimal):
                nr[k] = float(v)
            else:
                nr[k] = v
        out.append(nr)
    return out


# ---- CRUD (Add / View / Delete) ----------------------------------------------
def insert_expense(expense_date: str, amount: float, category: str, notes: str) -> None:
    logger.info(f"insert_expense {expense_date} {amount} {category} {notes!r}")
    with get_db_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO expenses (expense_date, amount, category, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (expense_date, amount, category, notes),
        )


def fetch_expenses_for_date(expense_date: str) -> List[Dict]:
    logger.info(f"fetch_expenses_for_date {expense_date}")
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT id, expense_date, amount, category, notes
            FROM expenses
            WHERE expense_date = %s
            ORDER BY id
            """,
            (expense_date,),
        )
        return _cast_numbers(cur.fetchall())


def delete_expenses_for_date(expense_date: str) -> None:
    logger.info(f"delete_expenses_for_date {expense_date}")
    with get_db_cursor(commit=True) as cur:
        cur.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


# ---- Summary (daily totals) --------------------------------------------------
def summary(start_date: str, end_date: str) -> List[Dict]:
    """
    Returns: [{"day": "YYYY-MM-DD", "total": float}, ...]
    """
    logger.info(f"summary {start_date}..{end_date}")
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT expense_date AS day, SUM(amount) AS total
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY day
            ORDER BY day
            """,
            (start_date, end_date),
        )
        return _cast_numbers(cur.fetchall())


# ---- Analytics (category totals + trend) -------------------------------------
def analytics_categories(start_date: str, end_date: str) -> List[Dict]:
    """
    Returns: [{"category": str, "total": float}, ...]
    """
    logger.info(f"analytics_categories {start_date}..{end_date}")
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category
            ORDER BY total DESC
            """,
            (start_date, end_date),
        )
        return _cast_numbers(cur.fetchall())


def analytics_category_trend(category: str, start_date: str, end_date: str) -> List[Dict]:
    """
    Returns: [{"day": "YYYY-MM-DD", "total": float}, ...]
    """
    logger.info(f"analytics_category_trend {category} {start_date}..{end_date}")
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT expense_date AS day, SUM(amount) AS total
            FROM expenses
            WHERE category = %s
              AND expense_date BETWEEN %s AND %s
            GROUP BY day
            ORDER BY day
            """,
            (category, start_date, end_date),
        )
        return _cast_numbers(cur.fetchall())
