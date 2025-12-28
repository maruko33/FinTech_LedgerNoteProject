from fastapi import APIRouter

from routers.v1.endpoints import users, accounts #, auth, journal_entries, budgets

router = APIRouter(prefix="/api/v1")

router.include_router(users.router)
router.include_router(accounts.router)