"""create chart table

Revision ID: ea2998888064
Revises: 91979b40eb38
Create Date: 2022-04-20 13:48:46.775855-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea2998888064'
down_revision = '91979b40eb38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ticket",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ticket", sa.String(50)),
    )
    op.create_table(
        "chart",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ticket_id", sa.Integer, sa.ForeignKey('ticket.id')),
        sa.Column("open", sa.Float),
        sa.Column("high", sa.Float),
        sa.Column("low", sa.Float),
        sa.Column("close", sa.Float),
        sa.Column("volume", sa.Float),
        sa.Column("date", sa.String(50)),
    )


def downgrade():
    op.drop_table("chart")
    op.drop_table("ticket")
