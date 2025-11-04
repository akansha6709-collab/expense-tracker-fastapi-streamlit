Expense Tracker (FastAPI + Streamlit + MySQL)

A full-stack expense management application that enables users to record daily expenses, view and filter spending, analyze category-wise trends, and track spending patterns over time.

This project demonstrates a modular full-stack setup using FastAPI, Streamlit, and MySQL, following clean separation of concerns between UI and REST API services.

✅ Features
Category	Capability
Add Expense	Date, category, amount, notes
View Expense	Filter by date range, table view
Delete Expense	Delete entries by date
Summary	Total spending by date range
Analytics	Category distribution & daily trend chart
Tech Stack	FastAPI + Streamlit + MySQL

## 🎥 Demo
[![Watch the demo](https://img.youtube.com/vi/a5KmQfWea8c/0.jpg)](https://youtu.be/a5KmQfWea8c)

🧱 Architecture
Project
│── Backend
│   ├── api.py                # FastAPI app + routes
│   ├── db_helper.py          # DB operations
│   ├── logging_setup.py
│   └── sql
│       ├── schema.sql
│       └── seed.sql
│
└── Frontend
    ├── app.py                # Streamlit entry point
    ├── AddUpdateUI.py
    ├── ViewDeleteUI.py
    ├── SummaryUI.py
    └── AnalyticsUI.py

🧠 Database Schema
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes VARCHAR(255)
);

⚙️ Setup Instructions
1️⃣ Clone Repo
git clone https://github.com/<your-username>/expense-tracker-fastapi-streamlit.git
cd expense-tracker-fastapi-streamlit

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment

Create .env:

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=exp_user
MYSQL_PASSWORD=MyAppPass#123
MYSQL_DB=expense_manager

4️⃣ Setup MySQL
mysql -u root -p

CREATE DATABASE expense_manager;
CREATE USER 'exp_user'@'%' IDENTIFIED BY 'MyAppPass#123';
GRANT ALL PRIVILEGES ON expense_manager.* TO 'exp_user'@'%';
FLUSH PRIVILEGES;


Load schema:

mysql -u exp_user -p expense_manager < Backend/sql/schema.sql
mysql -u exp_user -p expense_manager < Backend/sql/seed.sql

▶️ Run Services
Start FastAPI Backend
uvicorn Backend.api:app --reload


API Docs:
http://127.0.0.1:8000/docs

Start Streamlit Frontend
cd Frontend
streamlit run app.py


Set API URL inside the app:
http://127.0.0.1:8000

📡 API Examples
Add Expense (POST)
POST /expense
{
  "expense_date": "2025-01-10",
  "amount": 120.50,
  "category": "Food",
  "notes": "Lunch"
}

Get Expenses (GET)
GET /expenses?start_date=2025-01-01&end_date=2025-01-31

🧪 Testing
pytest

📊 Sample Analytics

Category spending bar chart

Daily spending line chart

Spending summary totals

🧰 Troubleshooting
Issue	Fix
MySQL connection refused	Ensure MySQL service is running
CORS error	Check FastAPI CORSMiddleware settings
API not reachable from Streamlit	Verify correct API URL
🚀 Future Roadmap

User authentication (JWT)

Docker deployment

Recurring expense reminders

Mobile-first UI

Multi-user support

📎 License

MIT License
