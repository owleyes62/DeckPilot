from app.models.deck import Deck
from app.schemas.deck import DeckCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DeckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: DeckCreate) -> Deck:
        deck = Deck(
            archetype=payload.archetype,
            play_style=payload.play_style,
            deck_json=payload.deck_json,
            win_condition=payload.win_condition,
            how_to_pilot=payload.how_to_pilot,
        )
        self.db.add(deck)
        await self.db.commit()
        await self.db.refresh(deck)
        return deck

    async def list_all(self) -> list[Deck]:
        result = await self.db.execute(select(Deck).order_by(Deck.id.desc()))
        return list(result.scalars().all())
