"""create table question_groups

Revision ID: ba3bef949137
Revises: b44adc0e8e3f
Create Date: 2024-08-19 14:40:31.599768

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "ba3bef949137"
down_revision = "b44adc0e8e3f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "question_groups",
        IdColumn(),
        sa.Column("name", sa.VARCHAR(), nullable=False),
    )


def downgrade():
    op.drop_table("question_groups")
