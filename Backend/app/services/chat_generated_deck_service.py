from app.repositories.chat_generated_deck_repository import \
    ChatGeneratedDeckRepository
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
