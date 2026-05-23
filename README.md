# 🏦 AI SQL Banking Chatbot System

## 📌 Introduction

AI SQL Banking Chatbot System is a mini core banking platform integrated with:

- MySQL Database
- Stored Procedures
- AI Fraud Detection
- AI Conversational Chatbot
- FastAPI Backend
- Machine Learning (Isolation Forest)

The system simulates a real banking environment where users can:

- Check balances
- Transfer money
- Withdraw money
- Repay loans
- Manage savings accounts
- Detect suspicious transactions using AI
- Interact with the banking system through natural language

---

# 🎯 Main Features

## 🏦 Core Banking

- Account management
- Transaction ledger
- Money transfer
- Withdrawal
- Savings account settlement
- Loan repayment

---

## 🤖 AI Features

- Fraud detection
- Transaction anomaly detection
- Risk scoring
- AI banking chatbot
- Intent classification
- Natural language banking interaction

---

# 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend + AI |
| FastAPI | REST API |
| MySQL | Database |
| SQLAlchemy | Database ORM |
| Scikit-learn | Machine Learning |
| Pandas | Data Processing |
| Isolation Forest | Fraud Detection |
| Uvicorn | API Server |

---

# 🏗️ System Architecture

```text
User
 ↓
AI Chatbot
 ↓
Intent Detection
 ↓
Banking Service Layer
 ↓
Stored Procedures
 ↓
MySQL Ledger Database
 ↓
Fraud Detection AI
 ↓
Risk Monitoring
```

---

# 📂 Project Structure

```text
banking_ai_chatbot/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── db.py
│   └── queries.py
│
├── ai/
│   ├── feature_engineering.py
│   ├── fraud_predictor.py
│   ├── train_model.py
│   ├── intent_classifier.py
│   └── entity_extractor.py
│
├── chatbot/
│   ├── router.py
│   └── response_builder.py
│
├── models/
│   └── isolation_forest.pkl
│
└── sql/
    ├── schema.sql
    └── procedures.sql
```

---

# ⚙️ Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/your-username/banking-ai-chatbot.git
```

---

## 2. Move Into Project

```bash
cd banking-ai-chatbot
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📦 requirements.txt Explanation

## ❓ What is `requirements.txt`?

`requirements.txt` is NOT a Python code file.

It is only a list of libraries that your project needs.

You DO NOT write Python code inside it.

Example:

```txt
fastapi
uvicorn
sqlalchemy
pymysql
pandas
numpy
scikit-learn
joblib
python-dotenv
```

---

# ❓ Do You Need To Code Inside requirements.txt?

✅ NO.

You only put library names.

Then install everything automatically using:

```bash
pip install -r requirements.txt
```

---

# 🧠 What Each Library Does

| Library | Purpose |
|---|---|
| fastapi | API backend |
| uvicorn | Run FastAPI server |
| sqlalchemy | Connect Python with MySQL |
| pymysql | MySQL driver |
| pandas | Process transaction data |
| numpy | Numerical computation |
| scikit-learn | Machine learning |
| joblib | Save/load AI model |
| python-dotenv | Environment variables |

---

# 🛠️ Database Setup

## Create Database

```sql
CREATE DATABASE banking;
```

---

## Import SQL Files

Run:

- schema.sql
- procedures.sql

inside MySQL Workbench.

---

# 🧾 Fraud Detection Table

```sql
CREATE TABLE fraud_detection (
    detect_id INT AUTO_INCREMENT PRIMARY KEY,

    trans_id VARCHAR(50),
    account_id VARCHAR(50),

    anomaly_score DECIMAL(10,5),
    risk_level VARCHAR(20),

    predicted_label INT,

    created_at DATETIME DEFAULT NOW()
);
```

---

# ⚙️ Configure Database Connection

## config.py

```python
DB_USER = "root"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_NAME = "banking"
```

Replace:

- username
- password
- database name

with your own MySQL configuration.

---

# 🤖 AI Fraud Detection

## Model Used

The system uses:

# Isolation Forest

for:

- anomaly detection
- suspicious transaction detection
- fraud risk scoring

---

# 📊 AI Features

The model learns transaction behavior using:

| Feature | Description |
|---|---|
| amount | transaction amount |
| balance | account balance |
| hour | transaction time |
| is_night | night transaction |
| large_transaction | high-value transfer |

---

# 🚀 Train AI Model

Run:

```bash
python ai/train_model.py
```

This will:

- read transaction history
- train the model
- save AI model into:

```text
models/isolation_forest.pkl
```

---

# 💬 AI Chatbot

The chatbot supports:

| User Request | Action |
|---|---|
| Check balance | Query balance |
| Transfer money | Call stored procedure |
| Transaction history | Query latest transactions |
| Loan inquiry | Query loan table |
| Savings inquiry | Query savings account |

---

# 🧠 Intent Detection

The chatbot detects user intentions such as:

- get_balance
- transfer
- withdraw
- repay_loan
- savings

---

# 🌐 Run API Server

```bash
uvicorn app:app --reload
```

Server runs at:

```text
http://127.0.0.1:8000
```

---

# 🧪 API Testing

## Home Endpoint

```text
GET /
```

---

## Chat Endpoint

```text
POST /chat
```

Example:

```text
message = "Số dư của tôi là bao nhiêu?"
account_id = "ACC001"
```

---

# 💸 Example Banking Operations

## Transfer Money

```text
Chuyển 5000000 sang ACC002
```

---

## Check Balance

```text
Số dư hiện tại là bao nhiêu?
```

---

## Transaction History

```text
Cho tôi xem lịch sử giao dịch
```

---

# 🚨 Fraud Detection Workflow

```text
Transaction
 ↓
Feature Extraction
 ↓
AI Model Prediction
 ↓
Risk Score
 ↓
Fraud Detection Table
```

---

# 📈 Risk Levels

| Score | Risk |
|---|---|
| LOW | Normal |
| MEDIUM | Suspicious |
| HIGH | Potential Fraud |

---

# 🔒 Security Features

- Transaction locking
- ACID transactions
- Stored procedure validation
- Fraud monitoring
- Risk scoring

---

# 🏦 Banking Procedures

The project includes:

| Procedure | Purpose |
|---|---|
| sp_chuyenKhoan | Money transfer |
| sp_rutTien | Withdraw money |
| sp_thanhToanNoHangThang | Loan repayment |
| sp_moSoTK | Open savings account |
| tat_toan_so_tiet_kiem | Savings settlement |

---

# 📚 Future Improvements

You can extend this project with:

- OpenAI GPT integration
- Voice banking assistant
- LangChain agents
- Kafka streaming
- Redis caching
- Real-time fraud detection
- OTP verification
- Mobile banking app
- Recommendation system

---

# 🎓 Educational Purpose

This project demonstrates:

- Database systems
- ACID transactions
- SQL stored procedures
- Machine learning integration
- AI chatbot systems
- Fraud detection
- Backend API development
- Banking system architecture

---

# 👨‍💻 Author

Your Name Here

---

# 📄 License

This project is for educational and research purposes.

