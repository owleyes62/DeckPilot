import json

from app.schemas.chat import (ChatGenerationStatus,
                              ChatMessageExchangeResponse, ChatMessageResponse)
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.app.services.ai.chat_ai_service import ChatAIService
from Backend.app.services.chat.chat_context_service import ChatContextService
from Backend.app.services.chat.chat_deck_context_service import \
    ChatDeckContextService
from Backend.app.services.chat.chat_generated_deck_service import \
    ChatGeneratedDeckService
from Backend.app.services.chat.chat_service import ChatService
from Backend.app.services.chat.chat_title_service import ChatTitleService
from Backend.app.services.decks.generated_deck_service import \
    GeneratedDeckService


class ChatOrchestratorService:
    def __init__(self, db: AsyncSession):
        self.chat_service = ChatService(db)
        self.chat_ai_service = ChatAIService()
        self.chat_context_service = ChatContextService()
        self.chat_deck_context_service = ChatDeckContextService(db)
        self.chat_generated_deck_service = ChatGeneratedDeckService(db)
        self.chat_title_service = ChatTitleService()
        self.generated_deck_service = GeneratedDeckService(db)

    async def _run_ai_until_final(
        self,
        session_id: int,
    ):
        messages = await self.chat_service.list_messages_by_session(
            session_id=session_id
        )
        session_context = self.chat_context_service.build_context(
            messages=messages)
        last_saved_deck = await self.chat_deck_context_service.get_last_saved_deck(
            session_id=session_id
        )

        step = self.chat_ai_service.get_next_step(
            messages=messages,
            session_context=session_context,
            last_saved_deck=last_saved_deck,
        )

        final_answer = self.chat_ai_service.parse_final_answer(step)
        return final_answer

    async def send_user_message(
        self,
        session_id: int,
        content: str,
    ) -> ChatMessageExchangeResponse:
        user_message = await self.chat_service.create_user_message(
            session_id=session_id,
            content=content,
        )

        messages = await self.chat_service.list_messages_by_session(
            session_id=session_id
        )

        visible_user_messages = [m for m in messages if m.role == "user"]
        if len(visible_user_messages) == 1:
            generated_title = self.chat_title_service.generate_title(messages)
            await self.chat_service.update_session_title(
                session_id=session_id,
                title=generated_title,
            )

        final_answer = await self._run_ai_until_final(session_id=session_id)

        assistant_message = await self.chat_service.create_assistant_message(
            session_id=session_id,
            content=final_answer.reply,
        )

        if (
            final_answer.deck_request is not None
            or final_answer.suggested_archetypes
            or final_answer.intent
        ):
            await self.chat_service.create_assistant_message(
                session_id=session_id,
                content="[CONTEXT_JSON] "
                + json.dumps(
                    {
                        "archetype": final_answer.deck_request.archetype
                        if final_answer.deck_request
                        else None,
                        "play_style": final_answer.deck_request.play_style
                        if final_answer.deck_request
                        else None,
                        "format": final_answer.deck_request.format
                        if final_answer.deck_request
                        else None,
                        "goal": final_answer.deck_request.goal
                        if final_answer.deck_request
                        else None,
                        "difficulty": final_answer.deck_request.difficulty
                        if final_answer.deck_request
                        else None,
                        "budget": final_answer.deck_request.budget
                        if final_answer.deck_request
                        else None,
                        "last_intent": final_answer.intent,
                        "last_reply_summary": final_answer.reply[:160],
                        "suggested_archetypes": [
                            item.name for item in final_answer.suggested_archetypes
                        ],
                        "notes": [
                            f"Sugestão anterior: {item.name} - {item.reason}"
                            for item in final_answer.suggested_archetypes
                        ],
                    },
                    ensure_ascii=False,
                ),
            )

        saved_deck = None
        saved_deck_detail = None
        invalid_cards: list[str] = []
        generation_status = ChatGenerationStatus(
            attempted=False,
            saved=False,
            message="Nenhum deck foi gerado nesta resposta.",
        )

        generated_deck = final_answer.generated_deck

        if generated_deck is not None:
            saved_deck, saved_deck_detail, invalid_cards, status_message = (
                await self.generated_deck_service.validate_and_save_generated_deck(
                    generated_deck
                )
            )

            # Segunda tentativa automática se a primeira geração falhar
            if saved_deck is None:
                await self.chat_service.create_assistant_message(
                    session_id=session_id,
                    content="[GENERATION_FEEDBACK] "
                    + json.dumps(
                        {
                            "status": "invalid_generated_deck",
                            "message": status_message,
                            "invalid_cards": invalid_cards,
                            "instruction": (
                                "Generate a corrected version, preserve deck identity, "
                                "avoid invented cards, and prefer a playable list."
                            ),
                        },
                        ensure_ascii=False,
                    ),
                )

                retry_answer = await self._run_ai_until_final(session_id=session_id)
                retry_generated_deck = retry_answer.generated_deck

                if retry_generated_deck is not None:
                    final_answer = retry_answer

                    assistant_message = await self.chat_service.create_assistant_message(
                        session_id=session_id,
                        content=final_answer.reply,
                    )

                    saved_deck, saved_deck_detail, invalid_cards, status_message = (
                        await self.generated_deck_service.validate_and_save_generated_deck(
                            retry_generated_deck
                        )
                    )

            generation_status = ChatGenerationStatus(
                attempted=True,
                saved=saved_deck is not None,
                message=status_message,
            )

            if saved_deck is not None:
                await self.chat_generated_deck_service.link_generated_deck(
                    session_id=session_id,
                    deck_id=saved_deck.id,
                    user_message_id=user_message.id,
                    assistant_message_id=assistant_message.id,
                )

        return ChatMessageExchangeResponse(
            session_id=session_id,
            user_message=ChatMessageResponse.model_validate(user_message),
            assistant_message=ChatMessageResponse.model_validate(
                assistant_message),
            ai_response=final_answer,
            saved_deck=saved_deck,
            saved_deck_detail=saved_deck_detail,
            invalid_cards=invalid_cards,
            generation_status=generation_status,
        )
