from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import UUID4, BaseModel, EmailStr


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserLoginInput(BaseModel):
    username: str
    password: str


class UserLoginOutput(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserRegisterInput(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole


class UserRegisterOutput(BaseModel):
    user_id: UUID4


class UserOutput(UserBase):
    user_id: UUID4


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class UserUpdateOutput(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[UserRole]


class Options(BaseModel):
    a: str
    b: str
    c: str
    d: str


class OptionEnum(str, Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"


class TypeEnum(str, Enum):
    python = "python"
    java = "java"
    csharp = "c#"


class MCQBase(BaseModel):
    type: str
    question: str
    options: Options
    correct_option: OptionEnum


class MCQCreate(MCQBase):
    pass


class MCQ(MCQBase):
    created_by: UUID4


class MCQDisplay(BaseModel):
    type: str
    mcq_id: UUID4
    question: str
    options: Options


class MCQCreateOutput(MCQBase):
    mcq_id: UUID4
    created_at: datetime


class AttemptedMcq(BaseModel):
    mcq_id: UUID4
    user_answer: OptionEnum


class SubmissionInput(BaseModel):
    attempted: List[AttemptedMcq]


class AttemptedMcqWithAnswer(BaseModel):
    mcq_id: UUID4
    type: str
    question: str
    options: Options
    correct_option: OptionEnum
    user_answer: OptionEnum


class SubmissionOutput(BaseModel):
    user_id: UUID4
    total_score: int
    total_attempts: int
    percentage: float
    data: List[AttemptedMcqWithAnswer]


class UserHistoryInput(BaseModel):
    user_id: UUID4
    total_score: float
    percentage: float
    total_attempts: int
    attempted_at: datetime


class PaginatedResponse(BaseModel):
    currentPage: int
    totalPage: int
    nextPage: Optional[int]
    totalCount: int
    data: List[Any]
