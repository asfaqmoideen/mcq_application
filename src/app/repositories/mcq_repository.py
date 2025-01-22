from typing import List, Optional
from uuid import UUID

from sqlalchemy import distinct
from sqlalchemy.orm import Session

from app.models.data_models import MCQ
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import MCQCreate


class McqRepository(BaseRepository[MCQ]):
    """A repository class for managing `MCQ` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the UserRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, mcq_id: UUID) -> MCQ:
        """
        Retrieve a single user by their UUID.

        Parameters: mcq_id : UUID

        Returns: MCQ
            The MCQ object

        """
        return self.session.query(MCQ).filter(MCQ.mcq_id == mcq_id).first()

    def get_all(
        self,
        type_: Optional[str] = None,
        question: Optional[str] = None,
    ) -> List[MCQ]:
        """
        Retrieve all mcq from the database.

        Returns: List[MCQ]
            A list of MCQ objects.
            unit_of_work.session.query(MCQ).filter_by(question=row.get("question")).first()
        """
        query = self.session.query(MCQ)

        if type_:
            query = query.filter(MCQ.type == type_)

        if question:
            query = query.filter(MCQ.question == question)

        return query.all()

    def add(self, mcq: MCQCreate) -> None:
        """
        Add a new MCQ to the database.

        Parameters: user : MCQCreate
            The mcq details for MCQCreate.
        """
        self.session.add(mcq)

    def update(self, mcq_id: UUID, **kwargs) -> None:
        """
        Update an MCQ with given fields.

        Parameters:
            mcq_id : UUID
                The unique identifier of the user to update.
            **kwargs : dict
                Key-value pairs of the attributes to update.
        """
        mcq = self.get(mcq_id)
        if mcq:
            for key, value in kwargs.items():
                setattr(mcq, key, value)

    def delete(self, mcq_id: UUID) -> bool:
        """
        Delete an MCQ by its ID.

        Parameters: user_id : UUID
            The unique identifier of the user to delete.
        """
        mcq = self.get(mcq_id)
        if mcq is None:
            return False
        self.session.delete(mcq)
        return True

    def get_mcq_types(self) -> list[str]:
        """
        Retrieve distinct types of MCQs.

        Returns:
            list[str]: List of distinct MCQ types.
        """
        return self.session.query(distinct(MCQ.type)).all()
