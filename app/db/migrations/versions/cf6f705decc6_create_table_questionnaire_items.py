"""create table questionnaire item

Revision ID: cf6f705decc6
Revises: ba3bef949137
Create Date: 2024-08-19 15:56:02.377991

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from enum import Enum, auto

import sqlalchemy as sa
from alembic import op

from app.db.migrations.drop_enum import drop_enum
from app.db.migrations.id_column import IdColumn

revision = "cf6f705decc6"
down_revision = "ba3bef949137"
branch_labels = None
depends_on = None


class questionnaire_item_type(str, Enum):  # type: ignore
    question = auto()
    group = auto()


def upgrade():
    op.create_table(
        "questionnaire_items",
        IdColumn(),
        sa.Column(
            "questionnaire_id",
            sa.Integer(),
            sa.ForeignKey("questionnaires.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("questions.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "question_group_id",
            sa.Integer(),
            sa.ForeignKey("question_groups.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("type", sa.Enum(questionnaire_item_type), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
    )
    op.create_index(
        "questionnaire_items__unique_order",
        "questionnaire_items",
        ["questionnaire_id", "order"],
        unique=True,
    )


def downgrade():
    op.drop_table("questionnaire_items")
    drop_enum(questionnaire_item_type)
