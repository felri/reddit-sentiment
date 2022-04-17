from pydantic import BaseModel
import typing as t


class CommentBase(BaseModel):
    body: str
    author: str
    created: str
    score: str
    permalink: str
    url: str
    prediction: str
    thread_id: int
    prediction: int


class CommentCreate(CommentBase):
    class Config:
        orm_mode = True


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
