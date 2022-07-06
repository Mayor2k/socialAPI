from ast import For
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Table
from sqlalchemy.types import Enum
import enum
from sqlalchemy.orm import relationship
from database import Base

class Genders(str, enum.Enum):
    male = "male"
    female = "female"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    gender = Column(Enum(Genders), nullable=False)
    birth_date = Column(Date, nullable=False)

    friends = relationship(
        "Friendship",
        primaryjoin = "or_(User.id == Friendship.user_a_id, User.id == Friendship.user_b_id)",
        viewonly = True
    )

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_a_id = Column(Integer, ForeignKey(User.id))
    user_b_id = Column(Integer, ForeignKey(User.id))


class UserFriendshipRequest(Base):
    __tablename__ = "users_friendship_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    requesting_user_id = Column(Integer, ForeignKey(User.id))
    receiving_user_id = Column(Integer, ForeignKey(User.id))