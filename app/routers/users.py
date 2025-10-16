from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user, UserAlreadyExistsError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_ep(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user = await create_user(session, payload.username, payload.email)
        return UserOut(id=user.id, username=user.username, email=user.email)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserOut)
async def get_user_ep(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=user.id, username=user.username, email=user.email)
