from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User

class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists"""
    pass

async def create_user(session: AsyncSession, username: str, email: str) -> User:
    u = User(username=username, email=email)
    session.add(u)
    try:
        await session.commit()
        await session.refresh(u)
        return u
    except IntegrityError as e:
        await session.rollback()
        # Check if it's a duplicate email or username error
        if "ix_users_email" in str(e):
            raise UserAlreadyExistsError(f"A user with email '{email}' already exists")
        elif "ix_users_username" in str(e):
            raise UserAlreadyExistsError(f"A user with username '{username}' already exists")
        else:
            raise

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    res = await session.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()
