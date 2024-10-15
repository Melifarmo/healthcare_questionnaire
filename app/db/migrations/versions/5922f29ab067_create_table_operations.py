"""Create table operations

Revision ID: 5922f29ab067
Revises: 4f3ae46ef01a
Create Date: 2024-10-15 22:02:53.917651

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa

from app.db.migrations.id_column import IdColumn

revision = '5922f29ab067'
down_revision = '4f3ae46ef01a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "operations",
        IdColumn(),
        sa.Column(
            "patient_id",
            sa.Integer(),
            sa.ForeignKey("patients.id"),
            nullable=False,
        ),
        sa.Column('operation_date', sa.Date, nullable=False)
    )


def downgrade():
    op.drop_table("operations")
