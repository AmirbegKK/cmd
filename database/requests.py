import random as rd

from sqlalchemy import select

from database.engine import session_maker
from database.models import Admin, Donate, Review, User


async def set_user(tg_id, name) -> None:
    """
    Записать нового юзера в бд если его не существует
    """
    
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id = tg_id, name=name))
            await session.commit()

async def set_admin(tg_id):
    """
    Записать нового админа в бд если его не существует
    """
    
    async with session_maker() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if not admin:
            session.add(Admin(tg_id = tg_id))
            await session.commit()
            return True
        
        return False


async def delete_admin(tg_id):
    """
    Удалить админа из бд
    """
    
    async with session_maker() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if admin:
            await session.delete(admin)
            await session.commit()
            return True
        
        return False


async def check_user_admin(tg_id):
    """
    Проверка, является ли пользователь администратором
    """
    
    async with session_maker() as session:
        user = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        
        if user:
            return True
        
        return False
    

async def get_users_id():
    """
    Получить список id всех пользователей
    """

    async with session_maker() as session:
        return await session.scalars(select(User.tg_id))


async def get_donats(limit: int, offset: int):
    """
    Получить список пожертвований
    """
    async with session_maker() as session:
        return await session.scalars(select(Donate).where(Donate.status == 4).offset(offset).limit(limit))


async def get_donate_by_id(donate_id: int):
    """
    Получить пожертвование по идентификатору
    """
    async with session_maker() as session:
        return await session.scalar(select(Donate).where(Donate.id == donate_id))


async def create_review(tg_id: int, text: str, review_type: int):
    """
    Создать отзыв
    """
    async with session_maker() as session:
        session.add(Review(tg_id=tg_id, text=text, type=review_type))
        await session.commit()


async def get_rand_donate(count):
    """
    Получить случайные пожертвования
    """
    

    async with session_maker() as session:
        donates = []
        for i in range(count):
            
            donate = await session.scalar(select(Donate).where(Donate.status == 4).offset(rd.randint(0, 2082)))
            if donate not in donates:
                donates.append(donate)
        return donates