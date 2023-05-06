from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, status

from app.v1.schema import todo_schema
from app.v1.schema.user_schema import User
from app.v1.service import todo_service
from app.v1.service.auth_service import get_current_user
from app.v1.utils.db import get_db

router = APIRouter(prefix="/api/v1/todo")


@router.get(
    "/",
    tags=["to-do"],
    status_code=status.HTTP_200_OK,
    response_model=List[todo_schema.Todo],
    dependencies=[Depends(get_db)],
)
def get_tasks(
    is_done: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user),
):
    """
    ## Get all tasks of a user by status

    ## Headers
    This endpoint requiere an authorization token

    ## Parameters
    This endpoint requiere the "is_done" param

    ### Returns
    - return the tasks list
    """
    return todo_service.get_tasks(current_user, is_done)


@router.get(
    "/{task_id}",
    tags=["to-do"],
    status_code=status.HTTP_200_OK,
    response_model=todo_schema.Todo,
    dependencies=[Depends(get_db)],
)
def get_task(
    task_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
):
    """
    ## Get an especific task

    ## Headers
    This endpoint requiere an authorization token

    ### Parameters
    The app require the id of the task
    - task_id: Id of the task


    ### Returns
    - return the task
    """
    return todo_service.get_task(task_id, current_user)


@router.post(
    "/",
    tags=["todo"],
    status_code=status.HTTP_201_CREATED,
    response_model=todo_schema.Todo,
    dependencies=[Depends(get_db)],
)
def create_task(
    todo: todo_schema.TodoCreate = Body(...),
    current_user: User = Depends(get_current_user),
):
    """
    ## Create task

    ## Headers
    This endpoint requiere an authorization token

    ### Args
    The app require the title of the task
    - title: Task title


    ### Returns
    - return created task
    """
    return todo_service.create_task(todo, current_user)


@router.patch(
    "/{task_id}/mark_done",
    tags=["to-do"],
    status_code=status.HTTP_200_OK,
    response_model=todo_schema.Todo,
    dependencies=[Depends(get_db)],
)
def mark_task_done(
    task_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
):
    """
    ## Update task as done

    ## Headers
    This endpoint requiere an authorization token

    ### Args
    The app require the id of the task
    - task_id: Id of the task


    ### Returns
    - return updated task
    """
    return todo_service.update_status_task(True, task_id, current_user)


@router.patch(
    "/{task_id}/unmark_done",
    tags=["to-do"],
    status_code=status.HTTP_200_OK,
    response_model=todo_schema.Todo,
    dependencies=[Depends(get_db)],
)
def unmark_task_done(
    task_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
):
    """
    ## Update task as not done

    ## Headers
    This endpoint requiere an authorization token

    ### Args
    The app require the id of the task
    - task_id: Id of the task


    ### Returns
    - return updated task
    """
    return todo_service.update_status_task(False, task_id, current_user)


@router.delete(
    "/{task_id}/",
    tags=["to-do"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_db)],
)
def delete_task(
    task_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_user),
):
    """
    ## Delete a task

    ## Headers
    This endpoint requiere an authorization token

    ### Args
    The app require the id of the task
    - task_id: Id of the task


    ### Returns
    - success message
    """
    todo_service.delete_task(task_id, current_user)

    return {"msg": "Task has been deleted successfully"}
