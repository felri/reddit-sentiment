"""create users table

Revision ID: 91979b40eb38
Revises: 
Create Date: 2020-03-23 14:53:53.101322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "91979b40eb38"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("first_name", sa.String(100)),
        sa.Column("last_name", sa.String(100)),
        sa.Column("address", sa.String(100)),
        sa.Column("hashed_password", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("is_superuser", sa.Boolean, nullable=False),
    )
    op.create_table(
        "redditor",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("comment_karma", sa.Integer),
    )
    op.create_table(
        "subreddit",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, unique=True),
        sa.Column("display_name", sa.String, unique=True),
        sa.Column("created", sa.String),
        sa.Column("public_description", sa.String),
        sa.Column("subscribers", sa.Integer),
    )
    op.create_table(
        "thread",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String),
        sa.Column("url", sa.String, unique=True,  nullable=False),
        sa.Column("author", sa.String),
        sa.Column("created", sa.String),
        sa.Column("num_comments", sa.Integer),
        sa.Column("score", sa.Integer),
        sa.Column("permalink", sa.String, unique=True,
                  nullable=False, index=True),
        sa.Column("selftext", sa.String),
        sa.Column("body", sa.String),
        sa.Column("prediction", sa.Integer),
        sa.Column("subreddit_id", sa.Integer, sa.ForeignKey('subreddit.id')),
    )
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("body", sa.String),
        sa.Column("author", sa.String),
        sa.Column("created", sa.String),
        sa.Column("score", sa.String),
        sa.Column("permalink", sa.String, unique=True,
                  nullable=False, index=True),
        sa.Column("url", sa.String),
        sa.Column("prediction", sa.Integer),
        sa.Column("thread_id", sa.Integer, sa.ForeignKey('thread.id')),
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("redditor")
    op.drop_table("subreddit")
    op.drop_table("thread")
    op.drop_table("comment")
