"""create table patients

Revision ID: 5ecb68b667f5
Revises: 6971286c5f18
Create Date: 2024-08-19 16:16:20.062736

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "5ecb68b667f5"
down_revision = "6971286c5f18"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patients",
        IdColumn(),
        sa.Column("full_name", sa.VARCHAR(), nullable=False),
        sa.Column("birthday_date", sa.Date(), nullable=False),
        sa.Column("phone", sa.VARCHAR(), nullable=False),
        sa.Column("passport_number", sa.VARCHAR(), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=True),
    )


def downgrade():
    op.drop_table("patients")
