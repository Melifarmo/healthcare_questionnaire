"""create table users


Revision ID: 6971286c5f18
Revises: 01064180f78e
Create Date: 2024-08-19 14:06:47.165279

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "6971286c5f18"
down_revision = "01064180f78e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        IdColumn(),
        sa.Column("full_name", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("password_hash", sa.VARCHAR(), nullable=False),
        sa.Column("password_salt", sa.VARCHAR(), nullable=False),
    )


def downgrade():
    op.drop_table("users")
