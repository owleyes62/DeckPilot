from app.repositories.deck_repository import DeckRepository
from app.schemas.deck import DeckCreate
from sqlalchemy.ext.asyncio import AsyncSession


class DeckService:
    def __init__(self, db: AsyncSession):
        self.repository = DeckRepository(db)

    async def create_deck(self, payload: DeckCreate):
        return await self.repository.create(payload)

    async def list_decks(self):
        return await self.repository.list_all()
