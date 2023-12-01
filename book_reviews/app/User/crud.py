from sqlalchemy.orm import Session
from ..models import User
from app.User.schemas import UserCreate

def get_user(db: Session, user_id:int):
    return db.query(User).filter(User.id==user_id).first()

def get_users(db: Session, skip : int = 0, limit: int =100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db : Session, user: UserCreate):
    fake_password = user.password = 'notreallyhashed'
    db_user =  User( name= user.user_name , password = fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

