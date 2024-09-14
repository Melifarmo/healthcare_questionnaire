"""Create table answer_options_groups

Revision ID: 697b8ce1c4f5
Revises: 8eb1ebc789df
Create Date: 2024-09-12 14:05:17.094256

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa

from app.db.migrations.id_column import IdColumn

revision = '697b8ce1c4f5'
down_revision = '8eb1ebc789df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "answer_options_groups",
        IdColumn(),
        sa.Column(
            "questionnaire_id",
            sa.Integer(),
            sa.ForeignKey("questionnaires.id"),
            nullable=False,
        ),
        sa.Column('name', sa.VARCHAR, nullable=False)
    )
    op.create_index(
        "answer_options_groups__unique_name",
        "answer_options_groups",
        ["name", "questionnaire_id"],
        unique=True,
    )


def downgrade():
    op.drop_table("answer_options_groups")
