from app.repositories.deck_repository import DeckRepository
from app.schemas.deck import DeckCreate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class DeckService:
    def __init__(self, db: AsyncSession):
        self.repository = DeckRepository(db)

    async def create_deck(self, payload: DeckCreate):
        if not payload.cards:
            raise HTTPException(
                status_code=400, detail="Deck must contain at least one card.")
        try:
            return await self.repository.create(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    async def list_decks(self):
        return await self.repository.list_all()

    async def get_deck_by_id(self, deck_id: int):
        return await self.repository.get_by_id(deck_id)
