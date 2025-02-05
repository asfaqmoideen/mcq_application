from abc import ABC

from app.config.database import get_db
from app.repositories.history_details_repository import HistoryDetailsRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.mcq_repository import McqRepository
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.user_repository import UserRepository


class BaseUnitOfWork(ABC):
    def __init__(self, session_factory=get_db):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = next(self.session_factory())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class UserUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.user = UserRepository(self.session)
        return self


class SubmissionUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.mcq = McqRepository(self.session)
        self.history = HistoryRepository(self.session)
        self.submission = SubmissionRepository(self.session)
        self.history_details = HistoryDetailsRepository(self.session)
        return self


class McqUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.mcq = McqRepository(self.session)
        self.submission = SubmissionRepository(self.session)
        return self


class HistoryUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.history = HistoryRepository(self.session)
        return self
