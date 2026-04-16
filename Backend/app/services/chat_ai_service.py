import json

from app.core.config import settings
from app.core.llm import get_groq_client
from app.core.prompt_loader import load_prompt
from app.models.chat_message import ChatMessage
from app.schemas.chat import ChatFinalAnswerResponse, ChatToolCallResponse
from app.schemas.chat_context import ChatSessionContext


class ChatAIService:
    def _build_conversation_history(self, messages: list[ChatMessage]) -> str:
        lines: list[str] = []

        for message in messages:
            role = message.role.upper()
            lines.append(f"{role}: {message.content}")

        return "\n".join(lines)

    def _call_model(self, conversation_history: str,
                    session_context: ChatSessionContext) -> dict:
        client = get_groq_client()

        system_prompt = load_prompt("chat/system.txt")
        user_template = load_prompt("chat/user_template.txt")
        user_prompt = user_template.format(
            conversation_history=conversation_history,
            session_context=json.dumps(
                session_context.model_dump(), ensure_ascii=False, indent=2),
        )

        response = client.chat.completions.create(
            model=settings.groq_model,
            temperature=0.4,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        content = response.choices[0].message.content or "{}"
        return json.loads(content)

    def get_next_step(self, messages: list[ChatMessage],
                      session_context: ChatSessionContext,
                      ) -> dict:
        conversation_history = self._build_conversation_history(messages)
        return self._call_model(conversation_history=conversation_history,
                                session_context=session_context,
                                )

    def parse_tool_call(self, payload: dict) -> ChatToolCallResponse:
        return ChatToolCallResponse(**payload)

    def parse_final_answer(self, payload: dict) -> ChatFinalAnswerResponse:
        return ChatFinalAnswerResponse(**payload)
