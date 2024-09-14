"""BaseRepository repository."""
import datetime
from abc import abstractmethod
from uuid import UUID

from pydantic import parse_obj_as
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUD
from app.db.sqlalchemy import Base
from app.schemas.base_scheme import BaseScheme


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._crud = CRUD(session=session, cls_model=self.model)

    @property
    @abstractmethod
    def model(self) -> Base:
        """Return repository model"""

    @property
    @abstractmethod
    def schema(self) -> Base:
        """Return model schema"""

    def _parse_to_schemas(self, instances: ScalarResult) -> list:
        return [parse_obj_as(self.schema, instance) for instance in instances]

    def _parse_to_schema(self, instance) -> BaseScheme:
        return parse_obj_as(self.schema, instance) if instance else None
