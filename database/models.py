from sqlalchemy import BigInteger, Column, DateTime, String, Text, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Donate(Base):
    __tablename__ = 'campaigns'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hashtag: Mapped[str] = mapped_column(String(255), nullable=False)
    goal : Mapped[int] = mapped_column(BigInteger)
    collected: Mapped[int] = mapped_column(BigInteger)
    user_count: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[int] = mapped_column(BigInteger)
    charity_id: Mapped[int] = mapped_column(BigInteger)
    help_receiver_count: Mapped[int] = mapped_column(BigInteger)
    link_open_event_count: Mapped[int] = mapped_column(BigInteger)
    published_at: Mapped[int] = mapped_column(DateTime(timezone=True), default=func.now())
    finished_at: Mapped[int] = mapped_column(DateTime(timezone=True), default=None)
    finish_payment_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(500), nullable=False)

