from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.schemas.mcq_schemas import (
    PaginatedResponse,
    SubmissionInput,
    SubmissionOutput,
    TypeEnum,
    UserHistoryInput,
    UserOutput,
)
from app.services import (
    HistoryUnitOfWork,
    McqUnitOfWork,
    SubmissionUnitOfWork,
    mcq_services,
    user_services,
)

router = APIRouter(tags=["MCQ Routes"])


@router.get("/mcq/types", response_model=list[TypeEnum])
def get_mcq_types(current_user: UserOutput = Depends(user_services.get_current_user)):
    """
    Endpoint to fetch distinct MCQ types.
    """
    unit_of_work = McqUnitOfWork()
    return mcq_services.fetch_mcq_types(unit_of_work=unit_of_work)


@router.get("/mcq/", response_model=PaginatedResponse)
async def get_random_mcqs(
    type: str = Query(..., description="MCQ type to filter by"),
    page_size: int = Query(10, le=100, description="Number of MCQs to attempt"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Fetches random MCQs of a chosen type, paginated by the given limit.

    Parameters:
    - type: MCQ type to filter the MCQs.
    - limit: Number of MCQs to return in the response (pagination).

    Returns:
    - List of MCQs based on the given type, paginated by the limit.
    """
    unit_of_work = McqUnitOfWork()
    mcqs = mcq_services.get_all(
        unit_of_work=unit_of_work,
        type=type,
        page_size=page_size,
        page=page,
        current_user=current_user,
    )
    return mcqs


@router.post("/mcq/submit", response_model=SubmissionOutput)
def submit_answers(
    submission: SubmissionInput,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to submit MCQ.
    """
    unit_of_work = SubmissionUnitOfWork()
    result = mcq_services.process_submission(
        submission=submission, unit_of_work=unit_of_work, current_user=current_user
    )
    return result


@router.post("/certificates/create")
def generate_certificate(
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to generate a certificate for a user based on their last MCQ submission.
    """
    unit_of_work = SubmissionUnitOfWork()
    result = mcq_services.create_certificate(
        unit_of_work=unit_of_work, current_user=current_user
    )
    return result


@router.get("/mcq/history", response_model=List[UserHistoryInput])
def user_submission_history(
    sort_by: str = Query(None, description="History to sort by"),
    order: str = Query("asc", description="sort order (asc/desc)"),
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to see user's submissions history.
    """
    unit_of_work = HistoryUnitOfWork()
    result = mcq_services.view_history_of_submission_of_user(
        unit_of_work=unit_of_work,
        current_user=current_user,
        sort_by=sort_by,
        order=order,
    )
    return result


@router.get("/mcq/history/{history_id}", response_model=SubmissionOutput)
def user_submission_history_by_id(
    history_id: UUID,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to see user's particular submission.
    """
    unit_of_work = SubmissionUnitOfWork()
    result = mcq_services.view_particular_history(
        unit_of_work=unit_of_work, current_user=current_user, history_id=history_id
    )
    return result
