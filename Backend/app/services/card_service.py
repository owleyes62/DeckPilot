from app.repositories.card_repository import CardRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CardService:
    def __init__(self, db: AsyncSession):
        self.repository = CardRepository(db)

    async def search_cards(self, query: str, limit: int = 20):
        return await self.repository.search_by_name(query=query, limit=limit)

    async def list_cards(self):
        return await self.repository.list_all()
