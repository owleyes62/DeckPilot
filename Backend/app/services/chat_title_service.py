from app.models.chat_message import ChatMessage


class ChatTitleService:
    def generate_title(self, messages: list[ChatMessage]) -> str:
        first_user_message = next(
            (message for message in messages if message.role == "user"),
            None,
        )

        if not first_user_message:
            return "Nova conversa"

        content = first_user_message.content.strip()

        if not content:
            return "Nova conversa"

        title = content[:60].strip()

        if len(content) > 60:
            title += "..."

        return title
