from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

PG_USER = "postgres"
PG_PASSWORD = "111"
PG_DB = "aiohttp_hw_db"
PG_HOST = "127.0.0.1"
PG_PORT = 5400
PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

Base = declarative_base()
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "users_adv"
    # id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # sqlalchemy 2.0+
    name = Column(String, nullable=False, unique=True)


class Advertisements(Base):
    __tablename__ = "advertisements_table"

    # id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    # owner_id = Column(Integer, ForeignKey("users_adv.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_adv.id"), nullable=False)


async def begin_s():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


async def end_s():
    await engine.dispose()


async def get_session():
    return Session()
