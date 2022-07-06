from operator import or_
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email = user.email, 
        hashed_password = fake_hashed_password, 
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        birth_date = user.birth_date)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_hashed_password(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first().hashed_password

def send_friendship_request(db: Session, from_user_id: int, to_user_id: int):
    db_friendship_request = models.UserFriendshipRequest(
        requesting_user_id = from_user_id,
        receiving_user_id = to_user_id)
    db.add(db_friendship_request)
    db.commit()
    db.refresh(db_friendship_request)
    return db_friendship_request

def get_user_friendship_requests(db: Session, user_id: int):
    return db.query(models.UserFriendshipRequest).filter(models.UserFriendshipRequest.requesting_user_id == user_id).all()

def get_user_friendship_receipts(db: Session, user_id: int):
    return db.query(models.UserFriendshipRequest).filter(models.UserFriendshipRequest.receiving_user_id == user_id).all()

def answer_to_friendship_request(db: Session, request_id: int, answer: bool):
    request = db.query(models.UserFriendshipRequest).filter(models.UserFriendshipRequest.id == request_id).first()
    
    if answer:
        db_friendship = models.Friendship(
            user_a_id = request.requesting_user_id,
            user_b_id = request.receiving_user_id
        )
        db.add(db_friendship)
        db.commit()
        db.refresh(db_friendship)

    db.delete(request)
    db.commit()
    return request

