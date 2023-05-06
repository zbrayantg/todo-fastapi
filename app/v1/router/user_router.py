from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.v1.schema import user_schema
from app.v1.schema.token_schema import Token
from app.v1.service import auth_service, user_service
from app.v1.utils.db import get_db

router = APIRouter(prefix="/api/v1", tags=["users"])


@router.post(
    "/user/",
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


@router.post("/login", tags=["users"], response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    ## Login for access token

    ### Args
    The app require the next fields by form data
    - username: Your username or email
    - password: Your password

    ### Returns
    - access token and token type
    """
    access_token = auth_service.generate_token(
        form_data.username, form_data.password
    )
    return Token(access_token=access_token, token_type="bearer")
