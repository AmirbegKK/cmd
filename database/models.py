from sqlalchemy import BigInteger, DateTime, String, func, ForeignKey, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    

class Donate(Base):
    __tablename__ = 'campaigns'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    hashtag: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[int] = mapped_column(BigInteger)
    collected: Mapped[int] = mapped_column(BigInteger)
    user_count: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[int] = mapped_column(BigInteger)
    charity_id: Mapped[int] = mapped_column(BigInteger)
    help_receiver_count: Mapped[int] = mapped_column(BigInteger)
    link_open_event_count: Mapped[int] = mapped_column(BigInteger)
    published_at: Mapped[int] = mapped_column(DateTime(timezone=True), default=func.now())
    finished_at: Mapped[int] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    finish_payment_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False)
