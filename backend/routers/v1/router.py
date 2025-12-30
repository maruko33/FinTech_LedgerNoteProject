from fastapi import APIRouter

from routers.v1.endpoints import users, accounts, journal_entries #, auth, budgets

router = APIRouter(prefix="/api/v1")

router.include_router(users.router)
router.include_router(accounts.router)
router.include_router(journal_entries.router)