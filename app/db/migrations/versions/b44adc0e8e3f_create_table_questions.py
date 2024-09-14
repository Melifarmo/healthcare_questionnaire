"""create table questions

Revision ID: b44adc0e8e3f
Revises: 8a2196328898
Create Date: 2024-08-14 11:29:45.736955

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from enum import Enum, auto

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Integer, ForeignKey

from app.db.migrations.drop_enum import drop_enum
from app.db.migrations.id_column import IdColumn

revision = "b44adc0e8e3f"
down_revision = "8a2196328898"
branch_labels = None
depends_on = None


class question_type(str, Enum):
    options = auto()
    text = auto()
    numeric = auto()


def upgrade():
    op.create_table(
        "questions",
        IdColumn(),
        sa.Column('answer_options_group_id', Integer, ForeignKey("answer_options_groups.id", ondelete="CASCADE")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("type", sa.Enum(question_type, name='question_type'), nullable=False),
        sa.Column("is_required", sa.Boolean(), server_default="true", nullable=False),
    )


def downgrade():
    op.drop_table("questions")
    drop_enum(question_type)
