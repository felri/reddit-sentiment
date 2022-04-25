from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from  sqlalchemy.sql.expression import func
import typing as t

from .. import models
from app.db.schemas.comment import Comment, CommentCreate


def get_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


def get_comment_by_permalink(db: Session, permalink: str) -> Comment:
    return db.query(models.Comment).filter(models.Comment.permalink == permalink).first()


def get_comments(
    db: Session, offset, limit
) -> t.List[Comment]:
    return db.query(models.Comment).order_by(func.random()).offset(offset).limit(limit).all()


def check_comment_exists(db: Session, permalink: str) -> bool:
    return db.query(models.Comment).filter(models.Comment.permalink == permalink).first() is not None


def create_comment(db: Session, comment: models.Comment):
    if check_comment_exists(db, comment.permalink):
        return None
    try:
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        print(e)
        return None


def delete_comment(db: Session, comment_id: int):
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Comment not found")
    db.delete(comment)
    db.commit()
    return comment


def edit_comment(
    db: Session, comment_id: int, comment: Comment
) -> Comment:
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Comment not found")
    update_data = comment.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_comment, key, value)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment_by_thread(
    db: Session, thread_id: int
) -> t.List[Comment]:
    return db.query(models.Comment).filter(models.Comment.thread_id == thread_id).all()


def get_comment_by_author(
    db: Session, author: str
) -> t.List[Comment]:
    return db.query(models.Comment).filter(models.Comment.author == author).all()
