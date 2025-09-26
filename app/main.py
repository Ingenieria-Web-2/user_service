""""
Main application entry point for the User microservice.
"""

from fastapi import FastAPI

from api.routers import user_router
from db.session import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users Microservice", root_path="/api/user")

app.include_router(user_router.router, tags=["user"])


@app.get("/")
def read_root():
    """
    Health check endpoint for the User microservice.
    """
    return {"service": "User Microservice is running"}
