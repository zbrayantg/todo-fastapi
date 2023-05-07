# Python
from datetime import datetime

# Pydantic
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=60, example="Realizar prueba técnica"
    )


class Todo(TodoCreate):
    id: int = Field(...)
    is_done: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
