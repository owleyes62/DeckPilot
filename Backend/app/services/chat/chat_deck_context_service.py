from app.schemas.card import CardResponse
from app.schemas.chat import ChatSavedDeckCard, ChatSavedDeckDetail
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.app.services.chat.chat_generated_deck_service import \
    ChatGeneratedDeckService


class ChatDeckContextService:
    def __init__(self, db: AsyncSession):
        self.chat_generated_deck_service = ChatGeneratedDeckService(db)

    async def get_last_saved_deck(self, session_id: int) -> ChatSavedDeckDetail | None:
        latest_link = await self.chat_generated_deck_service.get_latest_generated_deck(
            session_id=session_id
        )

        if not latest_link or not latest_link.deck:
            return None

        deck = latest_link.deck

        return ChatSavedDeckDetail(
            id=deck.id,
            name=deck.name,
            archetype=deck.archetype,
            play_style=deck.play_style,
            format=deck.format,
            win_condition=deck.win_condition,
            how_to_pilot=deck.how_to_pilot,
            source=deck.source,
            deck_cards=[
                ChatSavedDeckCard(
                    copies=item.copies,
                    section=item.section,
                    card=CardResponse.model_validate(item.card),
                )
                for item in deck.deck_cards
            ],
        )
