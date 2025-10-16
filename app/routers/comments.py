from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.comment import CommentCreate, CommentOut
from app.crud.comment import create_comment

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment_ep(post_id: int, payload: CommentCreate, session: AsyncSession = Depends(get_session)):
    c = await create_comment(session, post_id=post_id, text=payload.text, author_id=payload.author_id)
    return CommentOut.model_validate(c.__dict__)
