"""create table questionnaire

Revision ID: 5ed5b344e55a
Revises: 5ecb68b667f5
Create Date: 2024-08-19 14:52:29.272919

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "5ed5b344e55a"
down_revision = "5ecb68b667f5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "questionnaires",
        IdColumn(),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column(
            "requires_period", sa.Boolean(), nullable=False, server_default="false"
        ),
    )


def downgrade():
    op.drop_table("questionnaires")
