# LedgerNote

LedgerNote is an **append-only, double-entry ledger** API built with **FastAPI** and **MySQL**.  
It focuses on auditability and correctness: instead of mutating historical transactions, LedgerNote records changes via **reversal** and **correction** entries, preserving a complete, queryable history.

This repository is designed as a portfolio-grade backend project showcasing real-world engineering practices: authentication, data modeling, invariants, and financial reporting queries.

## Key Features

- **JWT Authentication**
  - Register / login
  - Protected endpoints via Bearer token
- **Ledger Accounts**
  - Create/list/get/update accounts
  - Account metadata (type, currency, name)
- **Journal Entries (Append-only)**
  - Create/list/get journal entries
  - Each entry contains multiple postings (double-entry)
- **Financial Invariants**
  - Minimum two postings per entry
  - `sum(amount_minor) = 0` enforced per entry (balanced transaction)
  - Uses integer minor units (e.g., cents) to avoid floating-point issues
- **Reporting**
  - **As-of Trial Balance**: grouped balances by account at a given timestamp
- **Audit Operations**
  - **Reversal** entry: neutralizes a prior entry
  - **Correction** entry: records an adjusted version while linking to the original

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL (Docker)
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Auth**: JWT

> Note: This project uses async DB sessions. The API is intended to be demoed via Swagger UI (`/docs`) or curl/Postman.

## Data Model (Conceptual)

### LedgerAccount
Represents an account (e.g., Cash, Bank, Revenue, Expense).

Typical fields:
- `id`
- `user_id`
- `name`
- `type` (e.g., ASSET / LIABILITY / EQUITY / INCOME / EXPENSE)
- `currency` (e.g., CAD)

### JournalEntry (Header)
Stores transaction metadata.

Typical fields:
- `id`
- `user_id`
- `occurred_at` (business effective timestamp)
- `description`
- `reversal_of_entry_id` (nullable; indicates this entry reverses another)
- `correction_of_entry_id` (nullable; indicates this entry corrects another)

### Posting (Lines)
Stores the actual debits/credits as signed integers in **minor units**.

Typical fields:
- `id`
- `entry_id`
- `account_id`
- `amount_minor` (signed integer, e.g., +10000 / -10000)
- `currency`

## Design Rules / Invariants

LedgerNote follows strict accounting-oriented rules:

1. **Append-only**
   - Historical journal entries are not mutated to “fix” mistakes.
2. **Double-entry**
   - Each journal entry has at least two postings.
   - The ledger enforces: `sum(amount_minor) = 0` per entry.
3. **Minor units**
   - Monetary values are stored as integers (e.g., cents) to avoid floating-point rounding.
4. **Audit links**
   - Reversal and correction entries link back to the original entry for traceability.

## API Overview

Swagger UI:
- `GET /docs`

Common endpoint groups (exact paths may vary depending on router prefixes in this repo):

- Auth
  - `POST /auth/register`
  - `POST /auth/login`
- Accounts
  - `POST /accounts`
  - `GET /accounts`
  - `GET /accounts/{account_id}`
- Journal Entries / Reports
  - `POST /journal-entries`
  - `GET /journal-entries`
  - `GET /journal-entries/{entry_id}`
  - `GET /journal-entries/trial-balance?as_of=...`
  - `POST /journal-entries/{entry_id}/reverse`
  - `POST /journal-entries/{entry_id}/correct`

## Quickstart (Local Development)

### Prerequisites

- Python 3.11+ (recommended)
- Docker + Docker Compose
- MySQL client (optional, for inspection)

### 1) Clone and configure environment

```bash
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_DIR>
cp .env.example .env
# Edit .env as needed
```

### 2) Start MySQL with Docker

```bash
docker compose up -d
```

### 3) Install dependencies

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

### 4) Run database migrations

```bash
alembic upgrade head
```

### 5) Start the API

```bash
uvicorn main:app --reload
```

Open:
- Swagger UI: `http://127.0.0.1:8000/docs`

> If your app entry is `backend/main.py` or `app/main.py`, adjust accordingly (e.g., `uvicorn app.main:app --reload`).

## Configuration

This repo expects environment variables via `.env`.

Typical variables (see `.env.example`):
- `DATABASE_URL` (async SQLAlchemy URL)
- `JWT_SECRET_KEY`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- Optional CORS settings

## Demo Walkthrough

You have two recommended demo modes:

1) **Swagger-first (recommended for interviews)**  
Open `http://127.0.0.1:8000/docs`, then:

- Register a user
- Login to obtain a JWT
- Click **Authorize** in Swagger and paste `Bearer <token>`
- Create two accounts (e.g., Cash and Income)
- Create a balanced journal entry with postings
- Query trial balance (as-of now)
- Reverse the entry and re-check trial balance
- Create a correction entry and re-check trial balance

2) **Scripted demo (curl)**  
See **`demo.md`** for a step-by-step script with curl examples.

## Project Structure

```text
backend/
├── alembic/               # migrations
├── models/                # SQLAlchemy models (users, accounts, entries, postings, ...)
├── schemas/               # Pydantic schemas (request/response models)
├── routers/               # FastAPI routers (auth, accounts, journal entries, reports)
├── crud/                  # DB operations and business logic
├── core/                  # core functions (config, DI, security, auth)
├── db/                    # AsyncSession factory, Base, engine
├── middleware/            # middleware
├── main.py                # FastAPI app entry
├── requirements.txt
├── .env.example
└── docker-compose.yml
```

## Error Behavior (High level)

- `401 Unauthorized`: missing/invalid token
- `404 Not Found`: resource not found (account/entry id)
- `400 Bad Request`: invariant violations (e.g., postings not balanced)

## Roadmap

- Budgets and budget lines
- More reports (income statement, balance sheet)
- Pagination, filtering, and export
- Deployment (Docker Compose full-stack, CI)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
