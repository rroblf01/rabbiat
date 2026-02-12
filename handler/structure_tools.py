from pydantic import BaseModel
from typing import Literal


class CityLocation(BaseModel):
    city: str
    country: str


class DatabaseStatus(BaseModel):
    name: str
    status: Literal["online", "offline", "maintenance"]


class UserInfo(BaseModel):
    name: str


class AllUserInfo(BaseModel):
    users: list[UserInfo]


class DatabaseWithUserInfo(BaseModel):
    database: DatabaseStatus
    users: list[UserInfo]
