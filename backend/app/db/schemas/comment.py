from pydantic import BaseModel
import typing as t


class CommentBase(BaseModel):
    body: str
    author: str = None
    created: str
    score: str
    permalink: str
    url: str = None
    thread_id: int
    prediction: int


class GetComments(BaseModel):
    offset: int
    limit: int


class CommentCreate(CommentBase):
    class Config:
        orm_mode = True


class CommentOut(BaseModel):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
