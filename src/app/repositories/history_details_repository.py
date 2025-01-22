from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.data_models import UserHistoryDetail
from app.repositories.base_repository import BaseRepository
from app.schemas.mcq_schemas import HistoryDetailsInput


class HistoryDetailsRepository(BaseRepository[UserHistoryDetail]):
    """A repository class for managing `UserHistoryDetail` objects in the database."""

    def __init__(self, session: Session):
        """
        Initialize the HistoryRepository with a database session.

        Parameters: session : Session(SQLAlchemy session object)
        """
        self.session = session

    def get(self, detail_id) -> UserHistoryDetail:
        """
        Retrieve a single History by their UUID.

        Parameters: history_id : UUID

        Returns: UserHistoryDetail
            The UserHistoryDetail object

        """
        submission = (
            self.session.query(UserHistoryDetail)
            .filter(UserHistoryDetail.history_id == detail_id)
            .first()
        )
        return submission

    def get_all(self, history_id) -> List[UserHistoryDetail]:
        """
        Retrieve all History from the database.

        Returns: List[UserHistoryDetail]
            A list of UserHistoryDetail objects.
        """
        query = self.session.query(UserHistoryDetail)

        if history_id:
            query = query.filter(UserHistoryDetail.history_id == history_id)

        return query.all()

    def add(self, history: HistoryDetailsInput):
        """
        Add a new History to the database.

        Parameters: user : HistoryDetailsInput
            The history details for HistoryDetailsInput.
        """
        self.session.add(history)

    def update(self, detail_id: UUID, **kwargs):
        pass

    def delete(self, detail_id: UUID):
        pass
