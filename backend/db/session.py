import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

DB_URI = os.environ["DATABASE_URL"]

engine = create_async_engine(
    DB_URI,
    echo = True,
    pool_size = 10,
    max_overflow = 10,
    pool_timeout = 10,
    pool_recycle = 3600,
    pool_pre_ping = True,

)

AsyncSessionFactory = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    autoflush = True,
    expire_on_commit = False
)