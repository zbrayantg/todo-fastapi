from fastapi import APIRouter, Body, Depends, status

from app.v1.schema import user_schema
from app.v1.service import user_service
from app.v1.utils.db import get_db

router = APIRouter(prefix="/api/v1")


@router.post(
    "/user/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.User,
    dependencies=[Depends(get_db)],
    summary="Create a new user",
)
def create_user(user: user_schema.UserRegister = Body(...)):
    """
    ## Create a new user

    ### Args
    The endpoint requiere the next args in JSON format.

    ```
    {
        "email": "A valid email",
        "username": "Unique username",
        "password": "Strong password"
    }
    ```

    ### Returns
    - user: User created info
    """
    return user_service.create_user(user)
