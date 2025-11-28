from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from db.database import get_db_session
from db.models import User
from schemas.entities import UserResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # i know that we must pass some env so only allowed origins can access api( for example only localhost:3000 and not 3001)  # noqa: E501
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "backend"}


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db_session)]):
    # i know that it is better to move logic to semo db repository and DAO to manipulate with data.
    # This is a quick solution
    users = db.query(User).options(joinedload(User.address), joinedload(User.credit_card)).all()
    return users
