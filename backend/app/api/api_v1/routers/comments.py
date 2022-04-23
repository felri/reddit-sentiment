from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.core.reddit import create_comments_via_praw
from app.db.crud.comment import (
    get_comments,
    get_comment,
    delete_comment,
    edit_comment,
)
from app.db.schemas.comment import CommentCreate, Comment, GetComments, CommentOut

comments_router = r = APIRouter()


@r.post(
    "/comments/",
    response_model=t.List[Comment],
    response_model_exclude_none=True,
)
async def comments_list(
    response: Response,
    body: GetComments,
    db=Depends(get_db),
):
    """
    Get all comments
    """
    comments = get_comments(db, body.offset, body.limit)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(comments)}"
    return comments

@r.get(
    "/comments/{comment_id}",
    response_model=Comment,
    response_model_exclude_none=True,
)
async def comment_details(
    request: Request,
    comment_id: int,
    db=Depends(get_db),
):
    """
    Get any comment details
    """
    comment = get_comment(db, comment_id)
    return comment
    # return encoders.jsonable_encoder(
    #     comment, skip_defaults=True, exclude_none=True,
    # )


@r.post("/create_comments/", response_model=CommentOut, response_model_exclude_none=True)
async def comment_create(
    request: Request,
    db=Depends(get_db),
):
    """
    Create a new comment
    """
    return create_comments_via_praw(db)


@r.put(
    "/comments/{comment_id}", response_model=Comment, response_model_exclude_none=True
)
async def comment_edit(
    request: Request,
    comment_id: int,
    comment: Comment,
    db=Depends(get_db),
):
    """
    Update existing comment
    """
    return edit_comment(db, comment_id, comment)


@r.delete(
    "/comments/{comment_id}", response_model=Comment, response_model_exclude_none=True
)
async def comment_delete(
    request: Request,
    comment_id: int,
    db=Depends(get_db),
):
    """
    Delete existing comment
    """
    return delete_comment(db, comment_id)
