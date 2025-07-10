# fastapi/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from time import sleep
from .database import engine, Base  # sync engine
from .routers import auth
from .routers import workouts 
from .routers import routines
# 🔁 Function to initialize DB (sync version)
def init_db_with_retry():
    max_tries = 10
    for attempt in range(max_tries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database is ready and tables created.")
            return
        except OperationalError as e:
            print(f"❌ Attempt {attempt+1}: DB not ready yet. Retrying in 2s...")
            sleep(2)
    raise Exception("❌ Could not connect to DB after retries.")

# 🔁 Initialize DB
init_db_with_retry()

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # fixed URL format
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Health check route
@app.get("/")
def health_check():
    return "Health check complete ✅"

# ✅ Include routers
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(routines.router)