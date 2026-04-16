from app.repositories.card_repository import CardRepository
from app.schemas.chat import ChatGeneratedDeck
from app.schemas.deck import DeckCreate, DeckListResponse
from app.schemas.deck_card import DeckCardCreate
from app.services.deck_service import DeckService
from sqlalchemy.ext.asyncio import AsyncSession


class GeneratedDeckService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.card_repository = CardRepository(db)
        self.deck_service = DeckService(db)

    async def validate_and_save_generated_deck(
        self,
        generated_deck: ChatGeneratedDeck,
    ) -> tuple[DeckListResponse | None, list[str]]:
        valid_cards: list[DeckCardCreate] = []
        invalid_cards: list[str] = []

        for item in generated_deck.cards:
            existing_card = await self.card_repository.get_by_name(item.name)

            if not existing_card:
                invalid_cards.append(item.name)
                continue

            valid_cards.append(
                DeckCardCreate(
                    name=existing_card.name,
                    copies=item.copies,
                    section=item.section,
                )
            )

        if not valid_cards:
            return None, invalid_cards

        payload = DeckCreate(
            name=generated_deck.name,
            archetype=generated_deck.archetype,
            play_style=generated_deck.play_style,
            format=generated_deck.format,
            win_condition=generated_deck.win_condition,
            how_to_pilot=generated_deck.how_to_pilot,
            source="generated",
            cards=valid_cards,
        )

        saved_deck = await self.deck_service.create_deck(payload)

        return (
            DeckListResponse.model_validate(saved_deck),
            invalid_cards,
        )
