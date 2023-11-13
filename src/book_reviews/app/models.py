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
    reviews = relationship("BookReview")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    books = relationship("Book")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    pub = Column(DateTime, nullable=False)
    author = Column(Integer, ForeignKey("authors.id"), nullable=False)


class BookReview(Base):
    __tablename__ = "book_reviews"

    id = Column(Integer, primary_key=True)
    desc = Column(Text, nullable=False)
    user = Column(Integer, ForeignKey("users.id"))
    book = Column(Integer, ForeignKey("books.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "review": self.review,
            "date": self.date,
        }

    def to_json(self):
        return dumps(self.to_dict())
