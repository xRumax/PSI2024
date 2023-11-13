from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List


# Define Pydantic models
class AuthorCreate(BaseModel):
    name: str


class Author(AuthorCreate):
    id: int

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author_id: int


class Book(BookCreate):
    id: int
    author: Author

    class Config:
        orm_mode = True


# Create an SQLite in-memory database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


# Define Author and Book classes
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")


# Create tables in the database
Base.metadata.create_all(engine)


# Dependency to get the database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Create a FastAPI route to get a book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
