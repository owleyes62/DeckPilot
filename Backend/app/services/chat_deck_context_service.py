import json

from app.models.chat_message import ChatMessage
from app.schemas.chat import ChatSavedDeckDetail


class ChatDeckContextService:
    def extract_last_saved_deck(self, messages: list[ChatMessage]) -> ChatSavedDeckDetail | None:
        for message in reversed(messages):
            content = message.content.strip()

            if not content.startswith("[SAVED_DECK_JSON]"):
                continue

            raw_json = content.removeprefix("[SAVED_DECK_JSON]").strip()

            try:
                data = json.loads(raw_json)
            except json.JSONDecodeError:
                continue

            return ChatSavedDeckDetail(**data)

        return None
