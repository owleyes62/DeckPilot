from app.schemas.chat import (ChatAIResponse, ChatMessageExchangeResponse,
                              ChatMessageResponse)
from app.services.chat_ai_service import ChatAIService
from app.services.chat_service import ChatService
from sqlalchemy.ext.asyncio import AsyncSession


class ChatOrchestratorService:
    def __init__(self, db: AsyncSession):
        self.chat_service = ChatService(db)
        self.chat_ai_service = ChatAIService()

    async def send_user_message(
        self,
        session_id: int,
        content: str,
    ) -> ChatMessageExchangeResponse:
        user_message = await self.chat_service.create_user_message(
            session_id=session_id,
            content=content,
        )

        messages = await self.chat_service.list_messages_by_session(session_id=session_id)

        ai_response: ChatAIResponse = self.chat_ai_service.generate_response(
            messages=messages)

        assistant_message = await self.chat_service.create_assistant_message(
            session_id=session_id,
            content=ai_response.reply,
        )

        return ChatMessageExchangeResponse(
            session_id=session_id,
            user_message=ChatMessageResponse.model_validate(user_message),
            assistant_message=ChatMessageResponse.model_validate(
                assistant_message),
            ai_response=ai_response,
        )
