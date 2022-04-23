from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from .. import models
from app.db.schemas.thread import ThreadCreate, Thread
from app.db.schemas.comment import Comment


def get_thread(db: Session, thread_id: int):
    thread = db.query(models.Thread).filter(
        models.Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


def get_thread_by_permalink(db: Session, permalink: str) -> Thread:
    return db.query(models.Thread).filter(models.Thread.permalink == permalink).first()


def get_threads(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[Thread]:
    return db.query(models.Thread).offset(skip).limit(limit).all()


def check_thread_exists_by_permalink(db: Session, thread_permalink: int):
    return db.query(models.Thread).filter(models.Thread.permalink == thread_permalink).first()


def create_thread(db: Session, thread: ThreadCreate):
    if(check_thread_exists_by_permalink(db, thread.permalink)):
        return None

    db_thread = models.Thread(**thread.dict())
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread


def delete_thread(db: Session, thread_id: int):
    thread = get_thread(db, thread_id)
    if not thread:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Thread not found")
    db.delete(thread)
    db.commit()
    return thread


def edit_thread(
    db: Session, thread_id: int, thread: Thread
) -> Thread:
    db_thread = get_thread(db, thread_id)
    if not db_thread:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Thread not found")
    update_data = thread.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_thread, key, value)

    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread


def get_thread_comments(
    db: Session, thread_id: int, skip: int = 0, limit: int = 100
) -> t.List[Comment]:
    return db.query(models.Comment).filter(models.Comment.thread_id == thread_id).offset(skip).limit(limit).all()


def get_comments_by_thread_id(
    db: Session, thread_id: int
) -> t.List[Comment]:
    return db.query(models.Comment).filter(models.Comment.thread_id == thread_id).all()