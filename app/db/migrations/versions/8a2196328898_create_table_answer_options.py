"""create table answer_options

Revision ID: 8a2196328898
Revises: 697b8ce1c4f5
Create Date: 2024-08-14 11:29:57.088740

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "8a2196328898"
down_revision = "697b8ce1c4f5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "answer_options",
        IdColumn(),
        sa.Column("answer_option_group_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("value", sa.VARCHAR(), nullable=True),
        sa.ForeignKeyConstraint(
            ("answer_option_group_id",), ["answer_options_groups.id"], onupdate="RESTRICT", ondelete="CASCADE"
        ),
    )


def downgrade():
    op.drop_table("answer_options")
