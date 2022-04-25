import os
import re
import praw
from fastapi import HTTPException, status
from prawcore import NotFound

import app.db.models as models
import app.db.crud.comment as comment_crud
import app.db.crud.thread as thread_crud
import app.db.crud.subreddit as subreddit_crud

from app.db.schemas.subreddit import SubredditCreate
from app.db.schemas.thread import ThreadCreate
from app.db.schemas.comment import CommentCreate


def get_reddit():
    return praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
    )


def sub_exists(sub, reddit=None):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def create_subreddit_via_praw(db, subreddit):
    reddit = get_reddit()
    if(sub_exists(subreddit, reddit)):
        sub = reddit.subreddit(subreddit)
        return subreddit_crud.create_subreddit(db, SubredditCreate(
            name=sub.display_name,
            display_name=sub.display_name,
            public_description=sub.public_description,
            subscribers=sub.subscribers,
            created=sub.created_utc,
        ))
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Subreddit not found")


def create_threads_via_praw(db, subreddit, flair='flair:"Daily+Discussion"', limit=10000):
    reddit = get_reddit()
    if(sub_exists(subreddit, reddit)):
        sub = subreddit_crud.get_subreddit_by_name(db, subreddit)

        if(sub is None):
            sub = create_subreddit_via_praw(db, subreddit)
            sub_instance = reddit.subreddit(sub.name)
            threads = sub_instance.search(flair, limit=limit)
        else:
            threads = reddit.subreddit(sub.name).search(flair, limit=limit)

        response = []
        for thread in threads:
            aux = thread_crud.create_thread(db, ThreadCreate(
                title=thread.title,
                url=thread.url,
                selftext=thread.selftext,
                score=thread.score,
                num_comments=thread.num_comments,
                created=thread.created_utc,
                permalink=thread.permalink,
                prediction=0,
                subreddit_id=sub.id,
            ))
            if(aux is not None):
                response.append(aux)
        return response
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Subreddit not found")


def clean_text(text):
    return remove_parentheses(remove_brakets(remove_urls(text)))


def remove_parentheses(text):
    return text.replace('(', '').replace(')', '')


def remove_brakets(text):
    return text.replace('[', '').replace(']', '')


def remove_urls(text):
    return re.sub(r'\b(?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)


def check_thread_has_comments(db, thread):
    thread_has_comments = thread_crud.get_comments_by_thread_id(db, thread.id)
    if(len(thread_has_comments) > 0):
        return True
    else:
        return False


def check_comment_validity(comment):
    if (hasattr(comment, 'body') and comment.body is not None and comment.body != '[deleted]' and comment.body != '[removed]'):
        return True
    else:
        return False


def get_author_name(comment):
    if(hasattr(comment, 'author')):
        if(comment.author is not None):
            return comment.author.name
        else:
            return 'Anonymous'
    else:
        return None


def create_comments_via_praw(db):
    reddit = get_reddit()

    threads = thread_crud.get_threads(db)
    response = []
    for thread in threads:
        print(thread.permalink)
        thread_instance = reddit.submission(
            url='https://reddit.com' + thread.permalink)
        if not check_thread_has_comments(db, thread):
            for comment in list(thread_instance.comments):
                if (check_comment_validity(comment)):
                    aux = comment_crud.create_comment(db, models.Comment(
                        body=clean_text(comment.body),
                        score=comment.score,
                        created=comment.created_utc,
                        permalink=comment.permalink,
                        thread_id=thread.id,
                        url=thread.url,
                        prediction=0,
                        author=get_author_name(comment),
                    ))
                    if(aux is not None):
                        print('Comment created for thread: ' + thread.title)
                        response.append(aux)
        else:
            print('Comments exists')

    return response
