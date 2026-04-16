from app.models.card import Card
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Card | None:
        normalized_name = name.strip().lower()
        result = await self.db.execute(
            select(Card).where(func.lower(Card.name) == normalized_name)
        )
        return result.scalar_one_or_none()

    async def get_by_external_id(self, external_id: int) -> Card | None:
        result = await self.db.execute(
            select(Card).where(Card.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def get_by_names(self, names: list[str]) -> list[Card]:
        normalized_names = [name.strip().lower()
                            for name in names if name.strip()]
        if not normalized_names:
            return []

        result = await self.db.execute(
            select(Card).where(func.lower(Card.name).in_(normalized_names))
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Card:
        card = Card(**kwargs)
        self.db.add(card)
        await self.db.flush()
        return card

    async def update(self, card: Card, **kwargs) -> Card:
        for key, value in kwargs.items():
            setattr(card, key, value)
        await self.db.flush()
        return card

    async def list_all(self) -> list[Card]:
        result = await self.db.execute(
            select(Card).order_by(Card.name.asc())
        )
        return list(result.scalars().all())

    async def search_by_name(self, query: str, limit: int = 20) -> list[Card]:
        normalized_query = f"%{query.strip().lower()}%"
        result = await self.db.execute(
            select(Card)
            .where(func.lower(Card.name).like(normalized_query))
            .order_by(Card.name.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def search_catalog(self, query: str, limit: int = 20) -> list[Card]:
        normalized_query = f"%{query.strip().lower()}%"

        result = await self.db.execute(
            select(Card)
            .where(
                or_(
                    func.lower(Card.name).like(normalized_query),
                    func.lower(func.coalesce(Card.card_type, "")
                               ).like(normalized_query),
                    func.lower(func.coalesce(Card.race, "")
                               ).like(normalized_query),
                    func.lower(func.coalesce(Card.attribute, "")
                               ).like(normalized_query),
                    func.lower(func.coalesce(Card.description, "")
                               ).like(normalized_query),
                )
            )
            .order_by(Card.name.asc())
            .limit(limit)
        )
        return list(result.scalars().all())
