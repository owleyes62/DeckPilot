from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Backend.app.models.chat.chat_generated_deck import ChatGeneratedDeck
from Backend.app.models.decks.deck import Deck
from Backend.app.models.decks.deck_card import DeckCard


class ChatGeneratedDeckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_next_generation_index(self, session_id: int) -> int:
        result = await self.db.execute(
            select(func.max(ChatGeneratedDeck.generation_index)).where(
                ChatGeneratedDeck.session_id == session_id
            )
        )
        current_max = result.scalar_one_or_none()
        return (current_max or 0) + 1

    async def create(
        self,
        session_id: int,
        deck_id: int,
        generation_index: int,
        user_message_id: int | None = None,
        assistant_message_id: int | None = None,
    ) -> ChatGeneratedDeck:
        link = ChatGeneratedDeck(
            session_id=session_id,
            deck_id=deck_id,
            generation_index=generation_index,
            user_message_id=user_message_id,
            assistant_message_id=assistant_message_id,
        )
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def get_latest_by_session(self, session_id: int) -> ChatGeneratedDeck | None:
        result = await self.db.execute(
            select(ChatGeneratedDeck)
            .options(
                selectinload(ChatGeneratedDeck.deck)
                .selectinload(Deck.deck_cards)
                .selectinload(DeckCard.card)
            )
            .where(ChatGeneratedDeck.session_id == session_id)
            .order_by(ChatGeneratedDeck.generation_index.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_by_session(self, session_id: int) -> list[ChatGeneratedDeck]:
        result = await self.db.execute(
            select(ChatGeneratedDeck)
            .options(
                selectinload(ChatGeneratedDeck.deck)
                .selectinload(Deck.deck_cards)
                .selectinload(DeckCard.card)
            )
            .where(ChatGeneratedDeck.session_id == session_id)
            .order_by(ChatGeneratedDeck.generation_index.asc())
        )
        return list(result.scalars().all())

    async def get_by_session_and_generation_index(
            self,
        session_id: int,
        generation_index: int,
    ) -> ChatGeneratedDeck | None:
        result = await self.db.execute(
            select(ChatGeneratedDeck)
            .options(
                selectinload(ChatGeneratedDeck.deck)
                .selectinload(Deck.deck_cards)
                .selectinload(DeckCard.card)
            )
            .where(ChatGeneratedDeck.session_id == session_id)
            .where(ChatGeneratedDeck.generation_index == generation_index)
            .limit(1)
        )
        return result.scalar_one_or_none()
