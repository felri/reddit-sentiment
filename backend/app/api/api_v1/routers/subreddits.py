from tokenize import String
from fastapi import Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.core.reddit import create_subreddit_via_praw
from app.db.crud.subreddit import (
    get_subreddits,
    get_subreddit,
    create_subreddit,
    delete_subreddit,
    edit_subreddit,
)
from app.db.schemas.subreddit import SubredditCreate, Subreddit
from .. import api_router

subreddits_router = r = api_router.APIRouter()

@r.get(
    "/subreddits",
    response_model=t.List[Subreddit],
    response_model_exclude_none=True,
)
async def subreddits_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all subreddits
    """
    subreddits = get_subreddits(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(subreddits)}"
    return subreddits


@r.get(
    "/subreddits/{subreddit_id}",
    response_model=Subreddit,
    response_model_exclude_none=True,
)
async def subreddit_details(
    request: Request,
    subreddit_id: int,
    db=Depends(get_db),
):
    """
    Get any subreddit details
    """
    subreddit = get_subreddit(db, subreddit_id)
    return subreddit


@r.post("/subreddit/{subreddit_name}", response_model=Subreddit, response_model_exclude_none=True)
async def subreddit_create(
    request: Request,
    subreddit_name: str,
    db=Depends(get_db),
):
    """
    Create a new subreddit
    """
    return create_subreddit_via_praw(db, subreddit_name)


@r.put(
    "/subreddits/{subreddit_id}", response_model=Subreddit, response_model_exclude_none=True
)
async def subreddit_edit(
    request: Request,
    subreddit_id: int,
    subreddit: Subreddit,
    db=Depends(get_db),
):
    """
    Update existing subreddit
    """
    return edit_subreddit(db, subreddit_id, subreddit)


@r.delete(
    "/subreddits/{subreddit_id}", response_model=Subreddit, response_model_exclude_none=True
)
async def subreddit_delete(
    request: Request,
    subreddit_id: int,
    db=Depends(get_db),
):
    """
    Delete existing subreddit
    """
    return delete_subreddit(db, subreddit_id)
