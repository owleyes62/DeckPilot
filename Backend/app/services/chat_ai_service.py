import json

from app.core.config import settings
from app.core.llm import get_groq_client
from app.core.prompt_loader import load_prompt
from app.models.chat_message import ChatMessage
from app.schemas.chat import ChatAIResponse


class ChatAIService:
    def _build_conversation_history(self, messages: list[ChatMessage]) -> str:
        lines: list[str] = []

        for message in messages:
            role = message.role.upper()
            lines.append(f"{role}: {message.content}")

        return "\n".join(lines)

    def generate_response(self, messages: list[ChatMessage]) -> ChatAIResponse:
        client = get_groq_client()

        system_prompt = load_prompt("chat/system.txt")
        user_template = load_prompt("chat/user_template.txt")

        conversation_history = self._build_conversation_history(messages)
        user_prompt = user_template.format(
            conversation_history=conversation_history)

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
        parsed = json.loads(content)

        return ChatAIResponse(**parsed)
