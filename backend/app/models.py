from pydantic import BaseModel, Field
from typing import Literal

class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200)
    type: Literal["person", "topic"]
    limit: int = Field(default=10, ge=1, le=25)

class JobResponse(BaseModel):
    job_id: str
    status: str
    expires_in_seconds: int

class Profile(BaseModel):
    id: str
    name: str
    headline: str
    location: str
    about: str
    profile_url: str
    experience: list[dict]
    education: list[dict]
    skills: list[str]
    fetched_at: str

class Post(BaseModel):
    id: str
    author: str
    text: str
    posted_at: str
    url: str
    engagement: dict
    topic: str | None = None
