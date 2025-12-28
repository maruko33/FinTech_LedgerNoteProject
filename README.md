# LedgerNote

LedgerNote is a personal finance ledger API built with FastAPI and MySQL.  
It uses an append-only ledger model: transactions are never overwritten; corrections are recorded as new entries to preserve an auditable history.

## Key Features

- Append-only ledger design with correction (reversal/adjustment) entries
- Accounts and transactions API (CRUD-oriented MVP)
- Category/tag support (optional)
- Budget and reporting endpoints (planned)
- Docker-based MySQL for local development
- Alembic migrations for schema evolution

## Tech Stack

- Backend: FastAPI, Python
- Database: MySQL (Docker)
- ORM: SQLAlchemy (async)
- Migrations: Alembic
- Tooling: Docker / docker-compose 

## Ledger Model (Concept)

LedgerNote follows an event-style accounting approach:

- Each transaction is immutable once written.
- If a transaction needs to be corrected, a new transaction is appended:
  - A reversal entry (negating the original)
  - An adjustment entry (the corrected values)
- Reports are derived from the ledger by aggregation rather than by mutating historical rows.

This pattern improves traceability and supports audit-friendly workflows.