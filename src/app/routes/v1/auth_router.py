from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.mcq_schemas import (
    UserLoginInput,
    UserLoginOutput,
    UserOutput,
    UserRegisterInput,
    UserRegisterOutput,
)
from app.services import UserUnitOfWork, user_services

router = APIRouter(prefix="/auth", tags=["Authentication"])
authorization_header_scheme = HTTPBearer()


@router.post("/register", response_model=UserRegisterOutput, status_code=201)
def register(register_data: UserRegisterInput):
    """
    User Registration endpoint
    """
    unit_of_work = UserUnitOfWork()
    return user_services.add(user=register_data, unit_of_work=unit_of_work)


@router.post("/login", response_model=UserLoginOutput)
def login(register_data: UserLoginInput):
    """
    User Registration endpoint
    """
    unit_of_work = UserUnitOfWork()

    return user_services.login(login_data=register_data, unit_of_work=unit_of_work)


@router.get("/me", response_model=UserOutput)
def me(current_user: UserOutput = Depends(user_services.get_current_user)):
    """
    Returns authenticated users details
    """
    return current_user


@router.post("/refresh", response_model=UserLoginOutput)
def refresh(
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    refresh token
    """
    if not token:
        raise HTTPException(status_code=401, detail="Authorization Header Not Provided")
    return user_services.refresh_token(token=token.credentials)
