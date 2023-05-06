import json

from fastapi import HTTPException, status

from app.v1.model.todo_model import Todo as TodoModel
from app.v1.schema import todo_schema, user_schema
from app.v1.utils.db import get_redis_pool


async def create_task(task: todo_schema.TodoCreate, user: user_schema.User):
    db_task = TodoModel(title=task.title, user_id=user.id)

    db_task.save()

    # Save task in Redis
    task_key = f"user:{user.id}:task:{db_task.id}"
    data = {
        "id": db_task.id,
        "title": db_task.title,
        "is_done": db_task.is_done,
        "created_at": db_task.created_at,
    }
    task_value = json.dumps(data, default=str)
    redis_pool = await get_redis_pool()
    await redis_pool.set(task_key, task_value)

    return todo_schema.Todo(
        id=db_task.id,
        title=db_task.title,
        is_done=db_task.is_done,
        created_at=db_task.created_at,
    )


async def get_tasks(user: user_schema.User, is_done: bool = None):
    if is_done is None:
        tasks_by_user = TodoModel.filter(
            TodoModel.user_id == user.id
        ).order_by(TodoModel.created_at.desc())
    else:
        tasks_by_user = TodoModel.filter(
            (TodoModel.user_id == user.id) & (TodoModel.is_done == is_done)
        ).order_by(TodoModel.created_at.desc())

    list_tasks = []
    redis_pool = await get_redis_pool()

    for task in tasks_by_user:
        task_json = await redis_pool.get(f"user:{user.id}:task:{task.id}")
        if task_json is not None:
            task_dict = json.loads(task_json)
        else:
            task_dict = task.__dict__["__data__"]
            del task_dict["user"]
            await redis_pool.set(
                f"user:{user.id}:task:{task.id}",
                json.dumps(task_dict, default=str),
            )
        list_tasks.append(todo_schema.Todo(**task_dict))

    return list_tasks


async def get_task(task_id: int, user: user_schema.User):
    redis_pool = await get_redis_pool()
    task_json = await redis_pool.get(f"user:{user.id}:task:{task_id}")
    if task_json is not None:
        task_dict = json.loads(task_json)
    else:
        db_task = TodoModel.filter(
            (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        task_dict = db_task.__dict__["__data__"]
        del task_dict["user"]
        await redis_pool.set(
            f"user:{user.id}:task:{db_task.id}",
            json.dumps(task_dict, default=str),
        )

    return todo_schema.Todo(**task_dict)


async def update_status_task(
    is_done: bool, task_id: int, user: user_schema.User
):
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    task.is_done = is_done
    task.save()

    task_dict = task.__dict__["__data__"]
    del task_dict["user"]

    redis_pool = await get_redis_pool()
    await redis_pool.set(
        f"user:{user.id}:task:{task.id}", json.dumps(task_dict, default=str)
    )

    return todo_schema.Todo(**task_dict)


async def delete_task(task_id: int, user: user_schema.User):
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    task.delete_instance()
    redis_pool = await get_redis_pool()
    await redis_pool.delete(f"user:{user.id}:task:{task.id}")
