from pydantic import BaseModel
import typing as t


class SubredditBase(BaseModel):
    name: str
    display_name: str
    created: str
    public_description: str
    subscribers: int


class SubredditCreate(SubredditBase):
    class Config:
        orm_mode = True


class Subreddit(SubredditBase):
    id: int

    class Config:
        orm_mode = True
