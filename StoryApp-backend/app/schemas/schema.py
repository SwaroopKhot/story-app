from pydantic import BaseModel, Field
from typing import Optional


class StoryBase(BaseModel):
    title: str
    content: str
    country: Optional[str] = None

class StoryCreate(StoryBase):
    pass

class StoryUpdate(StoryBase):
    pass

class StoryInDB(StoryBase):
    id: str
    author: str

    class Config:
        from_attributes = True
