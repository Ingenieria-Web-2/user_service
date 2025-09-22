from fastapi import FastAPI

from api.routers import user_router
from db.session import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users Microservice")

app.include_router(user_router.router, prefix="/api/user", tags=["user"])


@app.get("/")
def read_root():
    return {"service": "User Microservice is running"}
