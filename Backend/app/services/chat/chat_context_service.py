import json
from typing import Any

from app.models.chat_message import ChatMessage
from app.schemas.chat_context import ChatSessionContext


class ChatContextService:
    def build_context(self, messages: list[ChatMessage]) -> ChatSessionContext:
        context = ChatSessionContext()

        for message in messages:
            content = message.content.strip()

            if not content:
                continue

            # Tenta aproveitar mensagens de tool/final estruturadas salvas como texto cru
            if content.startswith("[CONTEXT_JSON]"):
                raw_json = content.removeprefix("[CONTEXT_JSON]").strip()

                try:
                    data: dict[str, Any] = json.loads(raw_json)
                except json.JSONDecodeError:
                    continue

                context.archetype = data.get("archetype") or context.archetype
                context.play_style = data.get(
                    "play_style") or context.play_style
                context.format = data.get("format") or context.format
                context.goal = data.get("goal") or context.goal
                context.difficulty = data.get(
                    "difficulty") or context.difficulty
                context.budget = data.get("budget") or context.budget
                context.last_intent = data.get(
                    "last_intent") or context.last_intent
                context.last_reply_summary = data.get(
                    "last_reply_summary") or context.last_reply_summary

                suggested = data.get("suggested_archetypes") or []
                for item in suggested:
                    if item and item not in context.suggested_archetypes:
                        context.suggested_archetypes.append(item)

                notes = data.get("notes") or []
                for note in notes:
                    if note not in context.notes:
                        context.notes.append(note)

            if content.startswith("[GENERATION_FEEDBACK]"):
                raw_json = content.removeprefix(
                    "[GENERATION_FEEDBACK]").strip()

                try:
                    data: dict[str, Any] = json.loads(raw_json)
                except json.JSONDecodeError:
                    continue

                feedback_message = data.get("message")
                if feedback_message:
                    context.notes.append(
                        f"Falha de geração anterior: {feedback_message}")

                invalid_cards = data.get("invalid_cards") or []
                for card_name in invalid_cards:
                    context.notes.append(
                        f"Carta inválida anterior: {card_name}")

        return context
