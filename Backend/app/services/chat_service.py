from app.repositories.chat_repository import ChatRepository
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class ChatService:
    def __init__(self, db: AsyncSession):
        self.repository = ChatRepository(db)

    async def create_session(self, title: str | None = None):
        session_title = (title or "Nova conversa").strip()
        if not session_title:
            session_title = "Nova conversa"

        return await self.repository.create_session(title=session_title)

    async def list_sessions(self):
        return await self.repository.list_sessions()

    async def get_session_by_id(self, session_id: int):
        session = await self.repository.get_session_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=404, detail="Chat session not found")
        return session

    async def create_user_message(self, session_id: int, content: str):
        await self.get_session_by_id(session_id)
        return await self.repository.create_message(
            session_id=session_id,
            role="user",
            content=content.strip(),
        )

    async def create_assistant_message(self, session_id: int, content: str):
        await self.get_session_by_id(session_id)
        return await self.repository.create_message(
            session_id=session_id,
            role="assistant",
            content=content.strip(),
        )

    async def list_messages_by_session(self, session_id: int):
        await self.get_session_by_id(session_id)
        return await self.repository.list_messages_by_session(session_id=session_id)
