"""create table periods

Revision ID: 8eb1ebc789df
Revises: 5ed5b344e55a
Create Date: 2024-08-21 20:29:23.307885

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "8eb1ebc789df"
down_revision = "5ed5b344e55a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "periods",
        IdColumn(),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column(
            "questionnaire_id",
            sa.Integer(),
            sa.ForeignKey("questionnaires.id"),
            nullable=False,
        ),
    )
    op.create_index(
        "periods__unique_name",
        "periods",
        ["name", "questionnaire_id"],
        unique=True,
    )


def downgrade():
    op.drop_table("periods")
