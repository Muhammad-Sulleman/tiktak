# fastapi/api/database.py

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/fastapi"
)

# 1. Async engine
async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # logs SQL queries
)

# 2. Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # avoid lazy reload after commits :contentReference[oaicite:1]{index=1}
)

# 3. Base for models
Base = declarative_base()

# # 4. Dependency for FastAPI
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
    
    