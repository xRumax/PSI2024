from sqlalchemy import ForeignKey, Boolean, Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship 

from .db import Base

class User(Base):
    __tablename__="users"

    id = Column("id", Integer, primary_key=True)
    user_name = Column("user_name", String)
    password = Column("password", String)
    admin = Column("admin", Boolean)

    reviews = relationship("Review", back_populates="creator")

class Book(Base):
    __tablename__="books"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    pub = Column("pub", DateTime)
    author_id = Column(Integer, ForeignKey("author.id"))
    
    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__="reviews"

    id = Column("id", Integer, primary_key=True)
    description = Column("description", String)
    rating = Column("rating", Float)
    book_id = Column(Integer, ForeignKey("books.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))

    book = relationship("Book", back_populates="reviews")
    creator = relationship("User", back_populates="reviews")
    

class Author(Base):
    __tablename__="author"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    birth_date = Column("birth_date", DateTime)

    books = relationship("Book", back_populates="author")

    
