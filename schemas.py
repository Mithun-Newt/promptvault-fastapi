from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class PromptBase(BaseModel):

    title: str
    content: str
    category: str


class PromptCreate(PromptBase):
    pass


class PromptResponse(PromptBase):

    id: int

    favorite: bool

    created_at: datetime

    class Config:

        orm_mode = True


class PromptPatch(BaseModel):

    title: Optional[str] = None

    content: Optional[str] = None

    category: Optional[str] = None

    favorite: Optional[bool] = None


class UserBase(BaseModel):

    username: str


class UserCreate(UserBase):

    password: str


class UserResponse(UserBase):

    id: int

    class Config:

        orm_mode = True

class UserLogin(BaseModel):

    username: str

    password: str