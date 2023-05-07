# Import the necessary modules and packages
from fastapi import FastAPI

from app.v1.router.todo_router import router as todo_router
from app.v1.router.user_router import router as user_router
from app.v1.scripts.create_db import create_db
from app.v1.scripts.create_tables import create_tables

# Create a new instance of the FastAPI class
app = FastAPI()

# Add the user_router and todo_router to the application
app.include_router(user_router)
app.include_router(todo_router)


@app.on_event("startup")
async def startup():
    create_db()
    create_tables()
