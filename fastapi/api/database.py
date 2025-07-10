# fastapi/api/database.py

import os
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/fastapi"
)

# 1. Async engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # logs SQL queries
)

# 2. Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 3. Base for models
Base = declarative_base()

# # 4. Dependency for FastAPI
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()
    
    