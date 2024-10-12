"""Create table question_tags

Revision ID: 4f3ae46ef01a
Revises: c95df3df8784
Create Date: 2024-10-09 22:38:34.491654

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import VARCHAR, ForeignKey

from app.db.migrations.drop_enum import drop_enum
from app.db.migrations.id_column import IdColumn

revision = '4f3ae46ef01a'
down_revision = 'c95df3df8784'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "question_group_tags",
        IdColumn(),
        sa.Column(
            'question_group_id',
            sa.Integer(),
            ForeignKey("question_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column('name', VARCHAR, nullable=False),
    )


def downgrade():
    op.drop_table("question_group_tags")
