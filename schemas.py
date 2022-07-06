from typing import List, Optional, Union
from datetime import date
from pydantic import BaseModel, Field
from enum import Enum

class Genders(str, Enum):
    male = "male"
    female = "female"

class UserFriendshipRequest(BaseModel):
    id: int
    requesting_user_id: int
    receiving_user_id: int

    class Config:
        orm_mode = True

class Friendship(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birth_date: date
    gender: Genders

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    friends: List[Friendship] = []

    def dict(self, **kwargs):
        data = super(User, self).dict(**kwargs)

        for friend in data['friends']:
            if data['id'] == friend['user_a_id']:
                friend['id'] = friend['user_b_id']
            elif data['id'] == friend['user_b_id']:
                friend['id'] = friend['user_a_id']

            del friend['user_a_id']
            del friend['user_b_id']

        return data

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None