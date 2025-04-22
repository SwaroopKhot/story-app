from pydantic import BaseModel
from typing import Optional

class StoryCreate(BaseModel):
    title: str
    content: str
    country: Optional[str] = None

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    country: Optional[str] = None

class StoryInDB(StoryCreate):
    id: str
    author: str
