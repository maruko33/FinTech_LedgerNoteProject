from fastapi import APIRouter, HTTPException, Depends
from schemas.journal_entries import JournalEntryCreate,JournalEntryOut,JournalEntryReversalIn,JournalEntryCorrectionIn
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_db, get_current_user, pagination_params
from models.user import User
from crud.journal_entries import create_journal_entry,list_journal_entries,get_journal_entries,reverse_journal_entries,correct_journal_entries

router = APIRouter(prefix="/journal_entry",tags=["journal_entry"])

@router.post("/", response_model=JournalEntryOut)
async def journal_entry_create(
    journal_entry_data: JournalEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_journal_entry(journal_entry_data,db,current_user.id)

@router.get("/", response_model=list[JournalEntryOut])
async def list_journals(
    page: tuple[int, int] = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    limit, offset = page
    return await list_journal_entries(db, current_user.id,limit,offset)

@router.get("/{id}", response_model=JournalEntryOut)
async def get_journal(
    id : int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_journal_entries(id,db,current_user.id)

@router.post("/{id}/reverse",response_model=JournalEntryOut)
async def reverse_journal(
    id : int,
    journal_reversal_data:JournalEntryReversalIn,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    return await reverse_journal_entries(id,journal_reversal_data, db, current_user.id)

@router.post("/{id}/correct", response_model=JournalEntryOut)
async def correct_journal(
    id: int,
    journal_correct_data: JournalEntryCorrectionIn,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):  
    await reverse_journal_entries(id,journal_correct_data, db, current_user.id)
    return await correct_journal_entries(
            id, journal_correct_data, db, current_user.id,
        )