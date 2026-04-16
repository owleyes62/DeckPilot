import json

from app.schemas.chat import ChatMessageExchangeResponse, ChatMessageResponse
from app.services.chat_ai_service import ChatAIService
from app.services.chat_service import ChatService
from app.services.chat_tool_service import ChatToolService
from sqlalchemy.ext.asyncio import AsyncSession


class ChatOrchestratorService:
    def __init__(self, db: AsyncSession):
        self.chat_service = ChatService(db)
        self.chat_ai_service = ChatAIService()
        self.chat_tool_service = ChatToolService(db)

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
        first_step = self.chat_ai_service.get_next_step(messages=messages)

        if first_step.get("type") == "tool_call":
            tool_call = self.chat_ai_service.parse_tool_call(first_step)

            tool_result = await self.chat_tool_service.execute_tool(
                tool_name=tool_call.tool_name,
                arguments=tool_call.arguments,
            )

            await self.chat_service.create_assistant_message(
                session_id=session_id,
                content=f"[TOOL_CALL] {tool_call.tool_name}: {json.dumps(tool_call.arguments, ensure_ascii=False)}",
            )

            await self.chat_service.create_assistant_message(
                session_id=session_id,
                content=f"[TOOL_RESULT] {json.dumps(tool_result, ensure_ascii=False)}",
            )

            messages = await self.chat_service.list_messages_by_session(session_id=session_id)
            second_step = self.chat_ai_service.get_next_step(messages=messages)
            final_answer = self.chat_ai_service.parse_final_answer(second_step)
        else:
            final_answer = self.chat_ai_service.parse_final_answer(first_step)

        assistant_message = await self.chat_service.create_assistant_message(
            session_id=session_id,
            content=final_answer.reply,
        )

        return ChatMessageExchangeResponse(
            session_id=session_id,
            user_message=ChatMessageResponse.model_validate(user_message),
            assistant_message=ChatMessageResponse.model_validate(
                assistant_message),
            ai_response=final_answer,
        )
