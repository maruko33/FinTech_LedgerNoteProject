# LedgerNote Demo Script (Swagger + curl)

This file is a short walkthrough you can run live.

## Assumptions

- Base URL: `http://127.0.0.1:8000`
- Swagger UI: `GET /docs`
- Routes roughly follow:
  - `/auth/*`
  - `/accounts/*`
  - `/journal-entries/*`

If your actual paths differ, open Swagger and use the displayed routes.

---

## Option A: Swagger Demo (Recommended)

1) Open `http://127.0.0.1:8000/docs`

2) Register  
`POST /auth/register`

Example body:
```json
{
  "email": "demo@example.com",
  "password": "DemoPassword123!"
}
```

3) Login and copy the token  
`POST /auth/login`

4) Click **Authorize** in Swagger  
Paste: `Bearer <access_token>`

5) Create two accounts  
`POST /accounts` (twice)

Example: Cash
```json
{ "name": "Cash", "type": "ASSET", "currency": "CAD" }
```

Example: Income
```json
{ "name": "Income", "type": "INCOME", "currency": "CAD" }
```

6) Create a balanced journal entry  
`POST /journal-entries`

Example (replace account ids):
```json
{
  "occurred_at": "2026-01-11T12:00:00Z",
  "description": "Demo: income received",
  "postings": [
    { "account_id": 1, "amount_minor": 10000, "currency": "CAD" },
    { "account_id": 2, "amount_minor": -10000, "currency": "CAD" }
  ]
}
```

Explain quickly:
- amounts are stored as integer minor units
- `sum(amount_minor) = 0` ensures double-entry balance
- journal entries are append-only

7) Trial balance (as-of)  
`GET /journal-entries/trial-balance?as_of=...`  
Try without `as_of` if your API defaults to “now”.

8) Reverse the entry  
`POST /journal-entries/{entry_id}/reverse`

9) Trial balance again (should net out)

10) Correct the original entry  
`POST /journal-entries/{entry_id}/correct`  
Submit the corrected postings payload (exact schema may vary).

---

## Option B: curl Demo (Scripted)

Export a token in your shell and call endpoints in order.


