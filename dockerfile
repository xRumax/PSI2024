FROM python:3.10-slim-buster

WORKDIR /app

ADD ./src/book_reviews /app
ADD ./pyproject.toml /app
ADD ./pdm.lock /app
ADD ./.pdm.toml /app

ENV PATH="/root/.cargo/bin:${PATH}"
ENV DATABASE_URL = "sqlite:///./db.db"

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN pip install pdm
RUN pdm sync


EXPOSE 80


CMD ["pdm", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]