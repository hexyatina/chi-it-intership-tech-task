from pydantic import BaseModel
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    username: str | None = None
    role: str | None = None