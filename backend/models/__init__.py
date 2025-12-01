from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URI = "mysql+asyncmy://fastapi:Mk.20021112@192.168.2.62:3306/carenote?charset=utf8mb4"

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

Base = declarative_base()