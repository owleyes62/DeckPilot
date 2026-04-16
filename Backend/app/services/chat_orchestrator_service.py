import json

from app.schemas.chat import (ChatGenerationStatus,
                              ChatMessageExchangeResponse, ChatMessageResponse)
from app.services.chat_ai_service import ChatAIService
from app.services.chat_context_service import ChatContextService
from app.services.chat_service import ChatService
from app.services.chat_title_service import ChatTitleService
from app.services.chat_tool_service import ChatToolService
from app.services.generated_deck_service import GeneratedDeckService
from sqlalchemy.ext.asyncio import AsyncSession


class ChatOrchestratorService:
    MAX_TOOL_STEPS = 4

    def __init__(self, db: AsyncSession):
        self.chat_service = ChatService(db)
        self.chat_ai_service = ChatAIService()
        self.chat_context_service = ChatContextService()
        self.chat_title_service = ChatTitleService()
        self.chat_tool_service = ChatToolService(db)
        self.generated_deck_service = GeneratedDeckService(db)

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

        visible_user_messages = [m for m in messages if m.role == "user"]
        if len(visible_user_messages) == 1:
            generated_title = self.chat_title_service.generate_title(messages)
            await self.chat_service.update_session_title(session_id=session_id, title=generated_title)

        final_answer = None

        for _ in range(self.MAX_TOOL_STEPS + 1):
            messages = await self.chat_service.list_messages_by_session(session_id=session_id)
            session_context = self.chat_context_service.build_context(
                messages=messages)

            step = self.chat_ai_service.get_next_step(
                messages=messages,
                session_context=session_context,
            )

            if step.get("type") == "tool_call":
                tool_call = self.chat_ai_service.parse_tool_call(step)

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

                continue

            final_answer = self.chat_ai_service.parse_final_answer(step)
            break

        if final_answer is None:
            raise ValueError(
                "A IA excedeu o número máximo de tool calls sem retornar resposta final.")

        assistant_message = await self.chat_service.create_assistant_message(
            session_id=session_id,
            content=final_answer.reply,
        )

        # salva snapshot simples de contexto inferido
        if final_answer.deck_request is not None or final_answer.suggested_archetypes:
            await self.chat_service.create_assistant_message(
                session_id=session_id,
                content="[CONTEXT_JSON] " + json.dumps(
                    {
                        "archetype": final_answer.deck_request.archetype if final_answer.deck_request else None,
                        "play_style": final_answer.deck_request.play_style if final_answer.deck_request else None,
                        "format": final_answer.deck_request.format if final_answer.deck_request else None,
                        "goal": final_answer.deck_request.goal if final_answer.deck_request else None,
                        "difficulty": final_answer.deck_request.difficulty if final_answer.deck_request else None,
                        "budget": final_answer.deck_request.budget if final_answer.deck_request else None,
                        "notes": [
                            f"Sugestão anterior: {item.name} - {item.reason}"
                            for item in final_answer.suggested_archetypes
                        ],

                    },
                    ensure_ascii=False,
                ),
            )

        saved_deck = None
        invalid_cards: list[str] = []
        generation_status = ChatGenerationStatus(
            attempted=False,
            saved=False,
            message="Nenhum deck foi gerado nesta resposta.",
        )

        if final_answer.generated_deck is not None:
            saved_deck, invalid_cards, status_message = await self.generated_deck_service.validate_and_save_generated_deck(
                final_answer.generated_deck)

            generation_status = ChatGenerationStatus(
                attempted=True,
                saved=saved_deck is not None,
                message=status_message,
            )

        return ChatMessageExchangeResponse(
            session_id=session_id,
            user_message=ChatMessageResponse.model_validate(user_message),
            assistant_message=ChatMessageResponse.model_validate(
                assistant_message),
            ai_response=final_answer,
            saved_deck=saved_deck,
            invalid_cards=invalid_cards,
            generation_status=generation_status,
        )
