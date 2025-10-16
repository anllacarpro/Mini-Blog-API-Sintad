from datetime import datetime
from pydantic import BaseModel

class CommentCreate(BaseModel):
    text: str
    author_id: int

class CommentOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_id: int
    post_id: int
