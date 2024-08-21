"""create table answer_options

Revision ID: 8a2196328898
Revises: b44adc0e8e3f
Create Date: 2024-08-14 11:29:57.088740

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "8a2196328898"
down_revision = "b44adc0e8e3f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "answer_options",
        IdColumn(),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("value", sa.VARCHAR(), nullable=True),
        sa.ForeignKeyConstraint(
            ("question_id",), ["questions.id"], onupdate="RESTRICT", ondelete="CASCADE"
        ),
    )


def downgrade():
    op.drop_table("answer_options")
