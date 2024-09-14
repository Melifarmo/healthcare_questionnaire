"""Subscription domain repository."""
from sqlalchemy import select

from app.db.base_repository import BaseRepository
from app.db.period.periods import PeriodModel

from app.schemas.period.period import Period


class PeriodRepo(BaseRepository):
    model = PeriodModel
    schema = Period

    async def get_periods(self) -> list[Period]:
        query = select(self.model)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

    async def get(self, period_id: int) -> Period | None:
        return await self._crud.get(pkey_val=period_id)
