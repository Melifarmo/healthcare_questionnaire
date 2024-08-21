from alembic import op
from sqlalchemy.dialects import postgresql


def drop_enum(enum):
    postgres_enum = postgresql.ENUM(enum)
    postgres_enum.drop(op.get_bind())
