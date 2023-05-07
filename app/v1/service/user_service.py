from fastapi import HTTPException, status

from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema
from app.v1.service.auth_service import get_password_hash


def create_user(user: user_schema.UserRegister):
    # Check if the user already exists with the same email or username
    get_user = UserModel.filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)
    ).first()
    if get_user:
        msg = "Email already registered"
        if get_user.username == user.username:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=msg
        )

    # Create a new user with the given details
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    # Save the user to the database
    db_user.save()

    # Return the created user
    return user_schema.User(
        id=db_user.id, username=db_user.username, email=db_user.email
    )
