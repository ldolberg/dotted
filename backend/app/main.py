from fastapi import FastAPI

from app.api.v1.endpoints import users

app = FastAPI()

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# TODO: Include routers for API endpoints 