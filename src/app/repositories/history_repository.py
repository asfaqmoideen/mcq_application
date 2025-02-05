from typing import List
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.data_models import UserHistory
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import UserHistoryInput


class HistoryRepository(BaseRepository[UserHistory]):
    """A repository class for managing `UserHistory` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the HistoryRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, history_id) -> UserHistory:
        """
        Retrieve a single History by their UUID.

        Parameters: history_id : UUID

        Returns: UserHistory
            The UserHistory object

        """
        submission = (
            self.session.query(UserHistory)
            .filter(UserHistory.history_id == history_id)
            .first()
        )
        return submission

    def get_all(
        self,
        user_id,
        sort_by: str = None,
        order: str = "asc",
    ) -> List[UserHistory]:
        """
        Retrieve all History from the database.

        Returns: List[UserHistory]
            A list of UserHistory objects.
        """
        query = self.session.query(UserHistory)

        if user_id:
            query = query.filter(UserHistory.user_id == user_id)

        if sort_by:
            if hasattr(UserHistory, sort_by):
                column = getattr(UserHistory, sort_by)
                query = query.order_by(
                    desc(column) if order.lower() == "desc" else column
                )

        return query.all()

    def add(self, history: UserHistoryInput):
        """
        Add a new History to the database.

        Parameters: user : UserHistoryInput
            The history details for UserHistoryInput.
        """
        self.session.add(history)

    def update(self, history_id: UUID, **kwargs):
        """
        Update History details.

        Parameters:
            history_id : UUID
                The unique identifier of the history to update.
            **kwargs : dict
                Key-value pairs of the attributes to update.
        """
        user = self.get(history_id)
        for key, value in kwargs.items():
            setattr(user, key, value)

    def delete(self, history_id: UUID):
        """
        Delete a user from the database.

        Parameters: history_id : UUID
            The unique identifier of the history to delete.
        """
        history = self.get(history_id)
        self.session.delete(history)
