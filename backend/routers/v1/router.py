from fastapi import APIRouter

from routers.v1.endpoints import users #, auth, accounts, journal_entries, budgets

router = APIRouter(prefix="/api/v1")

router.include_router(users.router)