from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class Redditor(Base):
    __tablename__ = "redditor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    comment_karma = Column(Integer)
    

class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String, unique=True,  nullable=False)
    author = Column(String)
    created = Column(String)
    num_comments = Column(Integer)
    score = Column(Integer)
    permalink = Column(String, unique=True,  nullable=False, index=True)
    selftext = Column(String)
    body = Column(String)
    children = relationship("Comment")
    prediction = Column(Integer)
    subreddit_id = Column(Integer, ForeignKey('subreddit.id'))


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    author = Column(String)
    created = Column(String)
    score = Column(String)
    permalink = Column(String, unique=True,  nullable=False, index=True)
    url = Column(String, unique=True,  nullable=False)
    prediction = Column(Integer)
    thread_id = Column(Integer, ForeignKey('thread.id'))


class Subreddit(Base):
    __tablename__ = "subreddit"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True,  nullable=False)
    display_name = Column(String)
    created = Column(String)
    public_description = Column(Integer)
    subscribers = Column(Integer)
    children = relationship("Thread")
