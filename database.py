from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "postgresql+psycopg://127.0.0.1/taskdb",
    connect_args={
        "user": "postgres",
        "password": "password",
    }
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass