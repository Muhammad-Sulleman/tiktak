from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, async_engine

from .routers import auth
from contextlib import asynccontextmanager
from api.database import async_engine, Base
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError
import asyncio
async def lifespan(app):
    max_tries = 10
    for attempt in range(max_tries):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database is ready and tables created.")
            break
        except OperationalError as e:
            print(f"❌ Attempt {attempt+1}: DB not ready yet. Retrying in 2s...")
            await asyncio.sleep(2)
    else:
        raise Exception("❌ Could not connect to DB after retries.")
    
    yield # This yields control to the app

    # (Optional) This runs on shutdown
    # You can add cleanup code here if needed

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http:localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)
@app.get('/')
def health_check():
    return "health check complete"
app.include_router(auth.router)