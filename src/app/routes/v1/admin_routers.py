from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

from app.schemas.mcq_schemas import (
    MCQ,
    MCQCreate,
    UserCreate,
    UserOutput,
    UserUpdate,
    UserUpdateOutput,
)
from app.services import McqUnitOfWork, UserUnitOfWork, mcq_services, user_services

router = APIRouter(tags=["Admin Routes"])


@router.get("/users", response_model=List[UserOutput])
def get_all_users(
    current_user: UserOutput = Depends(user_services.get_current_user),
) -> List[UserOutput]:
    """
    Get all users
    """
    unit_of_work = UserUnitOfWork()
    users = user_services.get_all(unit_of_work=unit_of_work, current_user=current_user)
    return users


@router.get("/users/{user_id}", response_model=UserOutput)
def get_one_user(
    user_id: UUID,
    current_user: UserOutput = Depends(user_services.get_current_user),
) -> UserOutput:
    """
    Get one user
    """
    unit_of_work = UserUnitOfWork()
    user = user_services.get(
        unit_of_work=unit_of_work, user_id=user_id, current_user=current_user
    )
    return user


@router.post("/users", status_code=201)
def add_user(
    user_details: UserCreate,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    add user
    """
    unit_of_work = UserUnitOfWork()
    user = user_services.add_user(
        unit_of_work=unit_of_work,
        user=user_details,
        current_user=current_user,
    )
    return user


@router.patch("/users/{user_id}", status_code=200)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: UserOutput = Depends(user_services.get_current_user),
) -> UserUpdateOutput:
    """
    update user details
    """
    unit_of_work = UserUnitOfWork()
    user = user_services.update(
        unit_of_work=unit_of_work,
        user_id=user_id,
        current_user=current_user,
        user_update=user_update,
    )
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Delete user
    """
    unit_of_work = UserUnitOfWork()
    user_services.delete(
        unit_of_work=unit_of_work, user_id=user_id, current_user=current_user
    )


@router.post("/bulk-upload", status_code=201)
def bulk_upload_mcqs(
    file: UploadFile = File(...),
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint for bulk uploading MCQs via an Excel file.

    Args:
        file (UploadFile): Excel file containing MCQ data.
        current_user (UserOutput): Current authenticated user.

    Returns:
        dict: Response message with the count of MCQs successfully added.
    """
    unit_of_work = McqUnitOfWork()
    mcq_count = mcq_services.bulk_add_mcqs(
        unit_of_work=unit_of_work, file=file, current_user=current_user
    )
    return {"message": f"{mcq_count} MCQs successfully added."}


@router.post("/mcq", status_code=201)
def create_mcq(
    mcq_data: MCQCreate,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to create a new MCQ.
    """
    unit_of_work = McqUnitOfWork()
    mcq_data = MCQ(**mcq_data.model_dump(), created_by=current_user.user_id)
    return mcq_services.add_mcq(
        mcq=mcq_data, unit_of_work=unit_of_work, current_user=current_user
    )
