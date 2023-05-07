from app.v1.model.todo_model import Todo
from app.v1.model.user_model import User
from app.v1.utils.db import db


def create_tables():
    # Use the database context manager to ensure that each database operation
    # is atomic, meaning that it either succeeds completely or fails completely
    with db:
        # Check if the User and Todo tables exist in the database, and create
        # them if they don't
        if not User.table_exists() or not Todo.table_exists():
            db.create_tables([User, Todo])
