from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from json import dumps
from .db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Integer, nullable=False)
    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan", lazy="joined"
    )


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    pub = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books", lazy="select")
    reviews = relationship(
        "Review", back_populates="book", cascade="all, delete-orphan", lazy="joined"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    desc = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="reviews")
