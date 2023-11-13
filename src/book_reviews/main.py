from fastapi import FastAPI
from app.book.routes import router as book_router
from app.containers import Container
from app.author.routes import router as author_router

container = Container()
app = FastAPI()


db = container.db()
db.create_database()
app.container = container
app.include_router(book_router, prefix="/api/book", tags=["book"])
app.include_router(author_router, prefix="/api/author", tags=["author"])
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
