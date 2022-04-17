from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from .. import models
from app.db.schemas.subreddit import Subreddit, SubredditCreate
from app.db.schemas.thread import Thread


def get_subreddit(db: Session, subreddit_id: int):
    subreddit = db.query(models.Subreddit).filter(
        models.Subreddit.id == subreddit_id).first()
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")
    return subreddit


def get_subreddit_by_name(db: Session, subreddit_name: str) -> Subreddit:
    return db.query(models.Subreddit).filter(models.Subreddit.name == subreddit_name).first()


def get_subreddits(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[Subreddit]:
    return db.query(models.Subreddit).offset(skip).limit(limit).all()


def create_subreddit(db: Session, subreddit: SubredditCreate):
    db_subreddit = models.Subreddit(
        name=subreddit.name,
        display_name=subreddit.display_name,
        created=subreddit.created,
        public_description=subreddit.public_description,
        subscribers=subreddit.subscribers,
    )
    db.add(db_subreddit)
    db.commit()
    db.refresh(db_subreddit)
    return db_subreddit


def delete_subreddit(db: Session, subreddit_id: int):
    subreddit = get_subreddit(db, subreddit_id)
    if not subreddit:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Subreddit not found")
    db.delete(subreddit)
    db.commit()
    return subreddit


def edit_subreddit(
    db: Session, subreddit_id: int, subreddit: Subreddit
) -> Subreddit:
    db_subreddit = get_subreddit(db, subreddit_id)
    if not db_subreddit:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Subreddit not found")
    update_data = subreddit.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_subreddit, key, value)

    db.add(db_subreddit)
    db.commit()
    db.refresh(db_subreddit)
    return db_subreddit


def get_subreddit_threads(
    db: Session, subreddit_id: int, skip: int = 0, limit: int = 100
) -> t.List[Thread]:
    return db.query(models.Thread).filter(models.Thread.subreddit_id == subreddit_id).offset(skip).limit(limit).all()
