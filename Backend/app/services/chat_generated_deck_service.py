from app.repositories.chat_generated_deck_repository import \
    ChatGeneratedDeckRepository
from app.schemas.chat import (ChatGeneratedDeckHistoryItem,
                              ChatGeneratedDeckHistoryResponse,
                              ChatSavedDeckSummary)
from sqlalchemy.ext.asyncio import AsyncSession


class ChatGeneratedDeckService:
    def __init__(self, db: AsyncSession):
        self.repository = ChatGeneratedDeckRepository(db)

    async def link_generated_deck(
        self,
        session_id: int,
        deck_id: int,
        user_message_id: int | None = None,
        assistant_message_id: int | None = None,
    ):
        generation_index = await self.repository.get_next_generation_index(session_id=session_id)
        return await self.repository.create(
            session_id=session_id,
            deck_id=deck_id,
            generation_index=generation_index,
            user_message_id=user_message_id,
            assistant_message_id=assistant_message_id,
        )

    async def get_latest_generated_deck(self, session_id: int):
        return await self.repository.get_latest_by_session(session_id=session_id)

    async def list_generated_decks(self, session_id: int):
        return await self.repository.list_by_session(session_id=session_id)

    async def get_generated_deck_history(
        self,
        session_id: int,
    ) -> ChatGeneratedDeckHistoryResponse:
        links = await self.repository.list_by_session(session_id=session_id)

        items: list[ChatGeneratedDeckHistoryItem] = []

        for link in links:
            if not link.deck:
                continue

            items.append(
                ChatGeneratedDeckHistoryItem(
                    generation_index=link.generation_index,
                    created_at=link.created_at,
                    deck=ChatSavedDeckSummary(
                        id=link.deck.id,
                        name=link.deck.name,
                        archetype=link.deck.archetype,
                        play_style=link.deck.play_style,
                        format=link.deck.format,
                        source=link.deck.source,
                    ),
                )
            )

        return ChatGeneratedDeckHistoryResponse(
            session_id=session_id,
            items=items,
        )
