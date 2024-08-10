from sqlalchemy import select

from database.engine import session_maker
from database.models import Donate, Review, User


async def set_user(tg_id, name) -> None:
    """
    Записать нового юзера в бд если его не существует
    """
    
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id = tg_id, name=name))
            await session.commit()


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


async def create_review(tg_id, text):
    """
    Создать отзыв
    """
    async with session_maker() as session:
        session.add(Review(tg_id=tg_id, text=text))
        await session.commit()
    