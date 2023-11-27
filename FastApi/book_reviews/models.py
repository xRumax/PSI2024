from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Text, DateTime
from .database import Base

class User(BaseModel):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False) 
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default= False)
    reviews = relationship()


class Review(BaseModel):
    id = Column(Integer, primary_key=True)
    desc = Column(Text, nullable=False)
    rating = Column(float, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator =relationship("User")
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book")


class Author(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(DateTime)
    books = relationship("Book", cascade="all")
