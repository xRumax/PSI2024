from fastapi import FastAPI
from app.book.routes import router as book_router
from app.containers import Container
from app.author.routes import router as author_router
from app.review.routes import router as review_router
from app.user.routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
container = Container()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = container.db()
db.create_database()
app.container = container
app.include_router(book_router, prefix="/api/book", tags=["book"])
app.include_router(author_router, prefix="/api/author", tags=["author"])
app.include_router(review_router, prefix="/api/review", tags=["review"])
app.include_router(user_router, prefix="/api/user", tags=["user"])

# żeby odpalić aplikację, wpisz w terminalu:
# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
