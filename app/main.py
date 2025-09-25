""""
Main application entry point for the User microservice.
"""

from fastapi import FastAPI

from api.routers import user_router
from db.session import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

# Configure documentation URLs to live under the same prefix used by the router.
# This makes the OpenAPI schema and Swagger UI available at /api/user/docs
# and the openapi.json at /api/user/openapi.json which works regardless of
# reverse-proxy URL rewriting behavior.
app = FastAPI(title="Users Microservice")

app.include_router(user_router.router, prefix="/api/user", tags=["user"])


@app.get("/")
def read_root():
    """
    Health check endpoint for the User microservice.
    """
    return {"service": "User Microservice is running"}
