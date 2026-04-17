from app.repositories.card_repository import CardRepository
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.app.models.cards.card import Card


class CardCatalogService:
    def __init__(self, db: AsyncSession):
        self.repository = CardRepository(db)

    def _serialize_card(self, card: Card) -> dict:
        return {
            "name": card.name,
            "card_type": card.card_type,
            "race": card.race,
            "attribute": card.attribute,
            "level": card.level,
            "atk": card.atk,
            "defense": card.defense,
            "description": card.description,
        }

    async def search_cards(self, query: str, limit: int = 20) -> list[dict]:
        cards = await self.repository.search_catalog(query=query, limit=limit)
        return [self._serialize_card(card) for card in cards]

    async def get_cards_by_names(self, names: list[str]) -> list[dict]:
        cards = await self.repository.get_by_names(names=names)
        return [self._serialize_card(card) for card in cards]

    async def get_archetype_candidates(self, archetype: str, limit: int = 30) -> list[dict]:
        cards = await self.repository.search_by_name(query=archetype, limit=limit)
        return [self._serialize_card(card) for card in cards]

    async def discover_cards_for_preferences(self, query: str, limit: int = 30) -> list[dict]:
        cards = await self.repository.search_catalog(query=query, limit=limit)
        return [self._serialize_card(card) for card in cards]
