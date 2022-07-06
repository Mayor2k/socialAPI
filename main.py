import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "b7ee50d6fd82427532ad7e200fee652798d413c45d80ea626b7be9cd5780d9f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token/")

'''@app.get("/api/")
async def say_hello(db: Session = Depends(get_db)):
    user = crud.get_user_hashed_password(db, user_email="string!")
    return user'''

@app.post("/api/token/")
async def get_auth_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    db_user_hashed_password = crud.get_user_hashed_password(db, user_email="string!")

    if not db_user_hashed_password == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/api/users/me/")
async def get_my_profile(token: str = Depends(oauth2_scheme)):
    return token

@app.get("/api/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/api/users/{user_id}", response_model=schemas.User)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/api/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/users/friendship/send/", response_model=schemas.UserFriendshipRequest, status_code=status.HTTP_201_CREATED)
async def send_friendship_request_to_user(user_a_id: int, user_b_id: int, db: Session = Depends(get_db)):
    frinedship  = crud.send_friendship_request(db, user_a_id, user_b_id)
    return frinedship

@app.post("/api/users/friendship/answer/", response_model=schemas.Friendship, status_code=status.HTTP_201_CREATED)
async def answer_to_frendship_request(request_id: int, answer: bool, db: Session = Depends(get_db)):
    request =  crud.answer_to_friendship_request(db, request_id=request_id, answer=answer)
    if request is None:
        raise HTTPException(status_code=404, detail="Friendship request not found")
    return request

if __name__ == "__main__":
    uvicorn.run("main:app", port = 8000, host = "127.0.0.1", reload = True)