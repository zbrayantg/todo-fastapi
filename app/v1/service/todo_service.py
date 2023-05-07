import json

from fastapi import HTTPException, status

from app.v1.model.todo_model import Todo as TodoModel
from app.v1.schema import todo_schema, user_schema
from app.v1.utils.db import get_redis_pool


async def create_task(task: todo_schema.TodoCreate, user: user_schema.User):
    # Create a new task in the database
    db_task = TodoModel(title=task.title, user_id=user.id)

    db_task.save()

    # Save task in Redis
    # Define the Redis key and value to store the task
    task_key = f"user:{user.id}:task:{db_task.id}"
    data = {
        "id": db_task.id,
        "title": db_task.title,
        "is_done": db_task.is_done,
        "created_at": db_task.created_at,
    }
    task_value = json.dumps(data, default=str)
    # Save the task in Redis using the key and value
    redis_pool = await get_redis_pool()
    await redis_pool.set(task_key, task_value)

    # Return the new task as a Todo object
    return todo_schema.Todo(
        id=db_task.id,
        title=db_task.title,
        is_done=db_task.is_done,
        created_at=db_task.created_at,
    )


async def get_tasks(user: user_schema.User, is_done: bool = None):
    # Get a list of tasks for a specific user
    if is_done is None:
        # If is_done is not specified, get all tasks for the user
        tasks_by_user = TodoModel.filter(
            TodoModel.user_id == user.id
        ).order_by(TodoModel.created_at.desc())
    else:
        # If is_done is specified, get tasks that match the status for the user
        tasks_by_user = TodoModel.filter(
            (TodoModel.user_id == user.id) & (TodoModel.is_done == is_done)
        ).order_by(TodoModel.created_at.desc())

    # Create an empty list to hold the tasks
    list_tasks = []
    # Get the Redis connection pool
    redis_pool = await get_redis_pool()

    # Loop through each task and add it to the list
    for task in tasks_by_user:
        # Try to get the task from Redis
        task_json = await redis_pool.get(f"user:{user.id}:task:{task.id}")
        if task_json is not None:
            # If the task is in Redis, convert it to a dictionary
            task_dict = json.loads(task_json)
        else:
            # If the task is not in Redis, get it from the database
            # Remove user field from the dictionary before saving it to Redis
            task_dict = task.__dict__["__data__"]
            del task_dict["user"]
            # Save the task in Redis
            await redis_pool.set(
                f"user:{user.id}:task:{task.id}",
                json.dumps(task_dict, default=str),
            )
        # Convert the task dictionary to a Todo object and add it to the list
        list_tasks.append(todo_schema.Todo(**task_dict))

    # Return the list of tasks
    return list_tasks


async def get_task(task_id: int, user: user_schema.User):
    # connect to Redis cache
    redis_pool = await get_redis_pool()
    # try to get task from Redis cache
    task_json = await redis_pool.get(f"user:{user.id}:task:{task_id}")
    if task_json is not None:
        # if task exists in Redis cache, load it as dictionary
        task_dict = json.loads(task_json)
    else:
        # if task not exists in Redis cache, get it from database
        db_task = TodoModel.filter(
            (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
        ).first()

        if not db_task:
            # if task not found in database, raise an exception
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        # convert database model instance to dictionary
        task_dict = db_task.__dict__["__data__"]
        # delete "user" key from task dictionary
        del task_dict["user"]
        # store task in Redis cache for future use
        await redis_pool.set(
            f"user:{user.id}:task:{db_task.id}",
            json.dumps(task_dict, default=str),
        )

    # return task as Todo object
    return todo_schema.Todo(**task_dict)


async def update_status_task(
    is_done: bool, task_id: int, user: user_schema.User
):
    # get task from database
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
    ).first()

    if not task:
        # if task not found in database, raise an exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # update the is_done field of task instance and save changes
    task.is_done = is_done
    task.save()

    # convert task instance to dictionary and del user
    task_dict = task.__dict__["__data__"]
    del task_dict["user"]

    # connect to Redis cache
    redis_pool = await get_redis_pool()
    # store updated task in Redis cache for future use
    await redis_pool.set(
        f"user:{user.id}:task:{task.id}", json.dumps(task_dict, default=str)
    )
    # return task as Todo object
    return todo_schema.Todo(**task_dict)


async def delete_task(task_id: int, user: user_schema.User):
    # Look up the task to delete by its ID and the ID of the user
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
    ).first()

    # If no matching task is found, raise an HTTP exception with a 404 status
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    # If a matching task is found, delete it from the database
    task.delete_instance()
    # Get a connection to the Redis server
    redis_pool = await get_redis_pool()
    # Remove the task's JSON data from the Redis cache
    await redis_pool.delete(f"user:{user.id}:task:{task.id}")
