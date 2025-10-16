from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment

async def create_comment(session: AsyncSession, post_id: int, text: str, author_id: int) -> Comment:
    c = Comment(text=text, post_id=post_id, author_id=author_id)
    session.add(c); await session.commit(); await session.refresh(c)
    return c
