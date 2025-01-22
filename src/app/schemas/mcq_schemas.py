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

    class Config:
        json_schema_extra = {
            "example": {
                "password": "john@12345",
                "username": "john",
            }
        }


class UserLoginOutput(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huIiwidXNlcm5hbWUiOiJqb2huIiwicm9sZSI6InVzZXIiLCJ1c2VyX2lkIjoiYTA1NzMyMGYtYmFlOS00M2VkLTk3NGEtYjJjZDgxZjg4ZjkzIiwiZXhwIjoxNzM2ODQ3Nzc2fQ.2rNhLoBZyuRK3EVUlY1OAq7aTfBThnxjxLn-4PkiMeI",
                "token_type": "Bearer",
            }
        }


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserRegisterInput(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john",
                "email": "john@example.com",
                "password": "john@12345",
            }
        }


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john",
                "email": "john@example.com",
                "password": "john@12345",
                "role": "user",
            }
        }


class UserRegisterOutput(BaseModel):
    user_id: UUID4

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "a057320f-bae9-43ed-974a-b2cd81f88f93",
            }
        }


class UserOutput(UserBase):
    user_id: UUID4

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john",
                "role": "user",
                "user_id": "a057320f-bae9-43ed-974a-b2cd81f88f93",
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

    class Config:
        json_schema_extra = {
            "example": {"username": "john", "email": "john@example.com", "role": "user"}
        }


class UserUpdateOutput(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[UserRole]

    class Config:
        json_schema_extra = {
            "example": {"username": "john", "email": "john@example.com", "role": "user"}
        }


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
    csharp = "csharp"


class MCQTypes(BaseModel):
    types: List[TypeEnum]

    class Config:
        json_schema_extra = {"example": {"types": ["python", "csharp", "java"]}}


class MCQBase(BaseModel):
    type: str
    question: str
    options: Options
    correct_option: OptionEnum


class MCQCreate(MCQBase):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "type": "python",
                "question": "Which of the following is a mutable data type in Python?",
                "options": {"a": "tuple", "b": "list", "c": "str", "d": "int"},
                "correct_option": "b",
            }
        }


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

    class Config:
        json_schema_extra = {
            "example": {
                "attempted": [
                    {
                        "mcq_id": "72ed3e01-ea48-481e-b060-d31ee8a74177",
                        "user_answer": "a",
                    }
                ]
            }
        }


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

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "9fbd245b-20b3-45a3-b81b-d3a32926981f",
                "total_score": 2,
                "total_attempts": 3,
                "percentage": 66.66666666666666,
                "data": [
                    {
                        "mcq_id": "72ed3e01-ea48-481e-b060-d31ee8a74177",
                        "type": "python",
                        "question": "What does the 'in' operator do in Python?",
                        "options": {
                            "a": "Checks if a value is present in a sequence",
                            "b": "Performs integer division",
                            "c": "Creates a new list",
                            "d": "string",
                        },
                        "correct_option": "a",
                        "user_answer": "a",
                    }
                ],
            }
        }


class UserHistoryInput(BaseModel):
    history_id: UUID4
    user_id: UUID4
    total_score: float
    percentage: float
    total_attempts: int
    attempted_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "history_id": "53cbd4eb-740f-4bbe-8e85-02db29d4218b",
                "user_id": "9fbd245b-20b3-45a3-b81b-d3a32926981f",
                "total_score": 1,
                "percentage": 100,
                "total_attempts": 1,
                "attempted_at": "2025-01-09T13:32:09.883204",
            }
        }


class PaginatedResponse(BaseModel):
    currentPage: int
    totalPage: int
    nextPage: Optional[int]
    totalCount: int
    data: List[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "currentPage": 1,
                "totalPage": 5,
                "nextPage": 2,
                "totalCount": 80,
                "data": [
                    {
                        "type": "python",
                        "mcq_id": "341458b1-87b5-440b-8324-8f013b353ade",
                        "question": "Which of the following is used to define a function in Python?",
                        "options": {
                            "a": "def",
                            "b": "function",
                            "c": "define",
                            "d": "lambda",
                        },
                    }
                ],
            }
        }
