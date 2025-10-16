from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.post import PostCreate, PostOut
from app.crud.post import create_post, get_latest_posts, get_post_with_comments

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostOut, status_code=201)
async def create_post_ep(payload: PostCreate, session: AsyncSession = Depends(get_session)):
    p = await create_post(session, payload.title, payload.content, payload.author_id)
    return PostOut.model_validate(p.__dict__)

@router.get("/", response_model=list[PostOut])
async def list_posts(limit: int = Query(10, ge=1, le=100), session: AsyncSession = Depends(get_session)):
    posts = await get_latest_posts(session, limit=limit)
    return [PostOut.model_validate(p.__dict__) for p in posts]

@router.get("/{post_id}", response_model=PostOut)
async def get_post_ep(post_id: int, session: AsyncSession = Depends(get_session)):
    p = await get_post_with_comments(session, post_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostOut.model_validate(p.__dict__)
