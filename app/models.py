from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from enum import Enum
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PermissionEnum(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    permissions: List[PermissionEnum] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TaskBase(BaseModel):
    description: str
    status: str = "pending"


class TaskCreate(TaskBase):
    agent_id: PyObjectId


class Task(TaskBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    agent_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class AgentBase(BaseModel):
    name: str


class Agent(AgentBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    tasks: List[PyObjectId] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
