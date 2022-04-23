from fastapi import  Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.core.reddit import create_threads_via_praw
from app.db.crud.thread import (
    get_threads,
    get_thread,
    create_thread,
    delete_thread,
    edit_thread,
)
from app.db.schemas.thread import ThreadCreate, Thread
from .. import api_router

threads_router = r = api_router.APIRouter()


@r.get(
    "/threads",
    response_model=t.List[Thread],
    response_model_exclude_none=True,
)
async def threads_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all threads
    """
    threads = get_threads(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(threads)}"
    return threads

@r.get(
    "/threads/{thread_id}",
    response_model=Thread,
    response_model_exclude_none=True,
)
async def thread_details(
    request: Request,
    thread_id: int,
    db=Depends(get_db),
):
    """
    Get any thread details
    """
    thread = get_thread(db, thread_id)
    return thread
    # return encoders.jsonable_encoder(
    #     thread, skip_defaults=True, exclude_none=True,
    # )

@r.post("/threads/{subreddit_name}", response_model=t.List[Thread], response_model_exclude_none=True)
async def subreddit_create(
    request: Request,
    subreddit_name: str,
    db=Depends(get_db),
):
    """
    Create a new subreddit
    """
    return create_threads_via_praw(db, subreddit_name)


@r.put(
    "/threads/{thread_id}", response_model=Thread, response_model_exclude_none=True
)
async def thread_edit(
    request: Request,
    thread_id: int,
    thread: Thread,
    db=Depends(get_db),
):
    """
    Update existing thread
    """
    return edit_thread(db, thread_id, thread)


@r.delete(
    "/threads/{thread_id}", response_model=Thread, response_model_exclude_none=True
)
async def thread_delete(
    request: Request,
    thread_id: int,
    db=Depends(get_db),
):
    """
    Delete existing thread
    """
    return delete_thread(db, thread_id)
