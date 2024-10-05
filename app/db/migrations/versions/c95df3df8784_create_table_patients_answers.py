"""create table patient_answers

Revision ID: c95df3df8784
Revises: 5ecb68b667f5
Create Date: 2024-08-19 14:06:59.444315

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from enum import Enum, auto

import sqlalchemy as sa
from alembic import op

from app.db.migrations.drop_enum import drop_enum
from app.db.migrations.id_column import IdColumn

revision = "c95df3df8784"
down_revision = "5ecb68b667f5"
branch_labels = None
depends_on = None


class patient_answer_type(str, Enum):  # type: ignore
    direct = auto()
    option = auto()
    bool = auto()


def upgrade():
    op.create_table(
        "patient_answers",
        IdColumn(),
        sa.Column(
            "patient_id",
            sa.Integer(),
            sa.ForeignKey("patients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("questions.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "questionnaire_id",
            sa.Integer(),
            sa.ForeignKey("questionnaires.id"),
            nullable=False,
        ),
        sa.Column(
            "period_id", sa.Integer(), sa.ForeignKey("periods.id"), nullable=True
        ),
        sa.Column(
            "answer_option_id",
            sa.Integer(),
            sa.ForeignKey("answer_options.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("type", sa.Enum(patient_answer_type, name='patient_answer_type')),
    )
    op.create_index(
        "patient_answers__unique_answer",
        "patient_answers",
        ["patient_id", "question_id", 'period_id', "questionnaire_id"],
        unique=True,
    )


def downgrade():
    op.drop_table("patient_answers")
    drop_enum(patient_answer_type)
