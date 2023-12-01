from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

db_url = "sqlite:///./app.db"

engine = create_engine(db_url, connect_args={"check_some_thread" : False})
Session = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()