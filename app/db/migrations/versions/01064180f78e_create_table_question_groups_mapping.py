"""create table question_groups_mapping

Revision ID: 01064180f78e
Revises: cf6f705decc6
Create Date: 2024-08-19 14:44:10.986723

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "01064180f78e"
down_revision = "cf6f705decc6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "question_groups_mapping",
        IdColumn(),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_group_id",
            sa.Integer(),
            sa.ForeignKey("question_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_index(
        "question_groups_mapping__unique_order",
        "question_groups_mapping",
        ["question_id", "question_group_id", "order"],
        unique=True,
    )


def downgrade():
    op.drop_table("question_groups_mapping")
