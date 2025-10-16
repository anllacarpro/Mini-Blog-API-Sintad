from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.post import Post

async def create_post(session: AsyncSession, title: str, content: str, author_id: int) -> Post:
    p = Post(title=title, content=content, author_id=author_id)
    session.add(p); await session.commit(); await session.refresh(p)
    return p

async def get_latest_posts(session: AsyncSession, limit: int = 10) -> list[Post]:
    res = await session.execute(select(Post).order_by(desc(Post.created_at)).limit(limit))
    return list(res.scalars().all())

async def get_post_with_comments(session: AsyncSession, post_id: int) -> Post | None:
    res = await session.execute(select(Post).where(Post.id == post_id))
    return res.scalar_one_or_none()
