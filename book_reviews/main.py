from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.User import crud, schemas
from app import models
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db= SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post("/users/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, name = user.user_name)
    return crud.create_user(db=db, user=user)

@app.get("/users/",response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit = limit)
    return users

@app.get("/users/{user_id}",response_model=list[schemas.User])
def get_user(user_id: int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
       
