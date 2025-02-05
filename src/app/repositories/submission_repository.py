from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.data_models import Submission
from app.repositories.base_repository import BaseRepository


class SubmissionRepository(BaseRepository[Submission]):
    """A repository class for managing `Submission` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the SubmissionRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, submission_id) -> Submission:
        """
        Retrieve a single submission by their UUID.

        Parameters: submission_id : UUID

        Returns: Submission
            The Submission object

        """
        submission = (
            self.session.query(Submission)
            .filter(Submission.submission_id == submission_id)
            .first()
        )
        return submission

    def get_all(
        self,
        submission_id: Optional[UUID] = None,
        user_id: Optional[int] = None,
        sort_by: str = "created_at",
        order: str = "asc",
    ) -> List[Submission]:
        """
        Retrieve all submission from the database.

        Returns: List[Submission]
            A list of Submission objects.
        """
        query = self.session.query(Submission)

        if submission_id:
            query = query.filter(Submission.submission_id == submission_id)

        if user_id:
            query = query.filter(Submission.user_id == user_id)

        if hasattr(Submission, sort_by):
            column = getattr(Submission, sort_by)
            query = query.order_by(desc(column) if order.lower() == "desc" else column)

        return query.all()

    def add(self, submission):
        """
        Add a new submission to the database.

        Parameters: submission
            The submissiont object.
        """
        self.session.add(submission)

    def update(self, detail_id: UUID, **kwargs):
        pass

    def delete(self, detail_id: UUID):
        pass
