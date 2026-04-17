from app.models.chat.chat_message import ChatMessage
from app.models.chat.chat_session import ChatSession
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, title: str = "Nova conversa") -> ChatSession:
        session = ChatSession(title=title)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def update_session_title(self, session_id: int, title: str) -> None:
        await self.db.execute(
            update(ChatSession)
            .where(ChatSession.id == session_id)
            .values(title=title)
        )
        await self.db.commit()

    async def get_session_by_id(self, session_id: int) -> ChatSession | None:
        result = await self.db.execute(
            select(ChatSession)
            .options(selectinload(ChatSession.messages))
            .where(ChatSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_sessions(self) -> list[ChatSession]:
        result = await self.db.execute(
            select(ChatSession).order_by(ChatSession.id.desc())
        )
        return list(result.scalars().all())

    async def create_message(
        self,
        session_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def list_messages_by_session(self, session_id: int) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id.asc())
        )
        return list(result.scalars().all())

    async def list_visible_messages_by_session(self, session_id: int) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .where(~ChatMessage.content.startswith("[TOOL_CALL]"))
            .where(~ChatMessage.content.startswith("[TOOL_RESULT]"))
            .where(~ChatMessage.content.startswith("[CONTEXT_JSON]"))
            .order_by(ChatMessage.id.asc())
        )
        return list(result.scalars().all())
