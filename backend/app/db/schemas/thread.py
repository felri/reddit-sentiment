from pydantic import BaseModel
import typing as t


class ThreadBase(BaseModel):
    title: str
    url: str
    selftext: str
    score: int
    num_comments: int
    created: str
    permalink: str
    prediction: int
    subreddit_id: int
    author: str = None


class ThreadCreate(ThreadBase):
    class Config:
        orm_mode = True


class Thread(ThreadBase):
    id: int

    class Config:
        orm_mode = True
