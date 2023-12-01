from sqlalchemy.orm import Session
from ..models import User
from schemas import *

def get_user(db: Session, user_id:int):
    return db.query(models.User)