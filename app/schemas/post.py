from datetime import datetime
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int
