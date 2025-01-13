from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import app_config
from app.models.data_models import User
from app.schemas.mcq_schemas import (
    UserCreate,
    UserLoginInput,
    UserLoginOutput,
    UserOutput,
    UserRegisterInput,
    UserUpdate,
    UserUpdateOutput,
)
from app.services.unit_of_work import BaseUnitOfWork
from app.utils.model_to_dict import model_to_dict

pwd_context = CryptContext(schemes=["bcrypt"])
authorization_header_scheme = HTTPBearer()


def get(
    user_id: UUID, unit_of_work: BaseUnitOfWork, current_user: UserOutput
) -> UserOutput:
    """
    Finds and returns a single user based on the UUID number

    Parameters
    ----------
    user_id: UUID
    unit_of_work: BaseUnitOfWork

    Returns
    -------

    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    with unit_of_work:
        target_user = unit_of_work.user.get(user_id=user_id)

        if target_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserOutput(**model_to_dict(target_user))


def add(user: UserRegisterInput, unit_of_work: BaseUnitOfWork):
    """
    adds user

    Parameters
    ----------
        user: UserRegisterInput (User Register object)
        unit_of_work: BaseUnitOfWork

    Returns
        user_id :  uuid of newly created user
    -------

    """
    with unit_of_work:
        try:
            user.password = get_password_hash(user.password)
            new_user = User(**user.model_dump())
            unit_of_work.user.add(user=new_user)
            unit_of_work.session.flush()
            unit_of_work.session.refresh(new_user)
            return {"user_id": str(new_user.user_id)}
        except ValueError as ve:
            unit_of_work.rollback()
            raise HTTPException(status_code=400, detail=str(ve))


def get_all(unit_of_work: BaseUnitOfWork, current_user: UserOutput) -> List[UserOutput]:
    """
    Finds and returns all users, accessible only to admin users.

    Parameters:
        unit_of_work: BaseUnitOfWork
        current_user: UserOutput (authenticated user's details)

    Returns
        List[UserOutput]: List of all users

    Raises
        HTTPException: If the user is not an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    with unit_of_work:
        users = unit_of_work.user.get_all()
        if users is None:
            raise HTTPException(status_code=404, detail="User not found")
        return [UserOutput(**model_to_dict(user)) for user in users]


def update(
    user_id: UUID,
    unit_of_work: BaseUnitOfWork,
    current_user: UserOutput,
    user_update: UserUpdate,
) -> UserUpdateOutput:
    """
    Update existing user

    Parameters:
        user_id: UUID
        unit_of_work: BaseUnitOfWork
        current_user: UserOutput (authenticated user's details)
        user_update: User detail schema object

    Returns:
        UserUpdateOutput
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    with unit_of_work:
        target_user = unit_of_work.user.get(user_id=user_id)
        if target_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        unit_of_work.user.update(
            user_id=user_id, **user_update.model_dump(exclude_none=True)
        )
    with unit_of_work:
        updated_user = unit_of_work.user.get(user_id=user_id)
        return UserUpdateOutput(**model_to_dict(updated_user))


def add_user(user: UserCreate, current_user: UserOutput, unit_of_work: BaseUnitOfWork):
    """
    adds user

    Parameters
    ----------
        user: UserCreate (User Object)
        unit_of_work: BaseUnitOfWork

    Returns
        user_id :  uuid of newly created user
    -------

    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )
    with unit_of_work:
        try:
            user.password = get_password_hash(user.password)
            new_user = User(**user.model_dump())
            unit_of_work.user.add(user=new_user)
            unit_of_work.session.flush()
            unit_of_work.session.refresh(new_user)
            return {"user_id": str(new_user.user_id)}
        except ValueError as ve:
            unit_of_work.rollback()
            raise HTTPException(status_code=400, detail=str(ve))


def delete(user_id: UUID, unit_of_work: BaseUnitOfWork, current_user: UserOutput):
    """
    Delete existing user

    Parameters:
        user_id: UUID
        unit_of_work: BaseUnitOfWork
        current_user: UserOutput (authenticated user's details)

    Returns:
        Bool
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )
    with unit_of_work:
        user = unit_of_work.user.delete(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")


def login(login_data: UserLoginInput, unit_of_work: BaseUnitOfWork) -> UserLoginOutput:
    """
    Authenticates user with password and username
    Args:
        login_data: LoginSchema containing username and password

    Returns:
        dict: containing access_token and token_type

    """
    with unit_of_work:
        user = unit_of_work.user.check_username_exists(login_data.username)
        if not check_user_access(user, login_data.password):
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        user_details = UserOutput(**user.__dict__).model_dump()
        access_token = create_access_token(data={"sub": user.username, **user_details})
        return UserLoginOutput(access_token=access_token, token_type="Bearer")
    return {"access_token": access_token, "token_type": "Bearer"}


def create_access_token(data: dict) -> str:
    """
    Creates access token using python-jose library
    Args:
        data: data to encode inside token
    Returns:
        str: created access token
    """
    to_encode = data.copy()
    to_encode["user_id"] = str(to_encode["user_id"])
    expire = datetime.utcnow() + timedelta(
        minutes=int(app_config["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, app_config["SECRET_KEY"], algorithm=app_config["ALGORITHM"]
    )
    return encoded_jwt


def check_user_access(user: User, password: str):
    """
    Checks if found user matches given password
    Args:
        user: user from db
        password: password from input

    Returns:
        bool: True if user matches, otherwise False

    """
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return True


def get_password_hash(password: str) -> str:
    """
    Creates hash from password using passlib library
    Args:
        password: raw password from input

    Returns:
        str: hashed password

    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies password using passlib library
    Args:
        plain_password: raw password from input
        hashed_password: hashed password from db

    Returns:
        bool: True if password matches otherwise False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
) -> UserOutput:
    """
    Retrieve the current authenticated user from the token.
    Parameters:
    ----------
    token : str (authorization token)

    Returns: UserOutput (authenticated user's details)

    Raises: HTTPException
        If the token is invalid or expired.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Authorization Header Not Provided")
    try:
        decoded_token = jwt.decode(
            token.credentials,
            app_config["SECRET_KEY"],
            algorithms=app_config["ALGORITHM"],
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Access Token Has Expired")
    except JWTError:
        raise HTTPException(status_code=500, detail="Invalid Token")

    return UserOutput(**decoded_token)


def refresh_token(token: str) -> dict:
    """
    refresh access token

    Args:
        token: current token

    Returns:
        dict: containing access_token and token_type

    """
    to_encode = jwt.decode(
        token, app_config["SECRET_KEY"], algorithms=app_config["ALGORITHM"]
    )
    access_token = create_access_token(to_encode)
    return {"access_token": access_token, "token_type": "Bearer"}
