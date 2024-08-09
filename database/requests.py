from sqlalchemy import select

from database.engine import session_maker
from database.models import Donate


async def get_donats(limit: int, offset: int):
    """
    Получить список пожертвований
    """
    async with session_maker() as session:
        return await session.scalars(select(Donate).offset(offset).limit(limit))


async def get_donate_by_id(donate_id: int):
    """
    Получить пожертвование по идентификатору
    """
    async with session_maker() as session:
        return await session.scalar(select(Donate).where(Donate.id == donate_id))