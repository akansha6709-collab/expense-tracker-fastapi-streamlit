# Expense Tracker (FastAPI + Streamlit + MySQL)

A complete end-to-end expense management system with backend API and interactive UI.

## 🧾 Features
- Add / update expenses
- View / delete expenses
- Summary by date range
- Category-wise analytics with charts
- SQLite storage + FastAPI REST backend
- Streamlit frontend

## 🛠️ Tech Stack
### Backend
- FastAPI
- Pydantic
- SQLite
- SQLAlchemy
- pytest (tests)

### Frontend
- Streamlit
- Pandas
- Requests

## 🚀 Run Project

### 1️⃣ Start Backend
## 🛠️ Backend Installation

```bash
pip install -r requirements.txt
uvicorn Backend.api:app --reload --port 8000

## 🚀 Run Locally

### 1️⃣ Create virtual env
python -m venv venv
source venv/Scripts/activate  # Windows PowerShell

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Run backend (FastAPI)
uvicorn Backend.api:app --reload --port 8000

### 4️⃣ Run frontend (Streamlit)
streamlit run Frontend/app.py --server.port 8502
