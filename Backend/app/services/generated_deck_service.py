from app.repositories.card_repository import CardRepository
from app.schemas.chat import ChatGeneratedDeck, ChatSavedDeckSummary
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
    ) -> tuple[ChatSavedDeckSummary | None, list[str], str]:
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
            return None, invalid_cards, "Nenhuma carta gerada foi encontrada no catálogo local."

        main_count = sum(
            card.copies for card in valid_cards if card.section == "main")
        extra_count = sum(
            card.copies for card in valid_cards if card.section == "extra")
        side_count = sum(
            card.copies for card in valid_cards if card.section == "side")

        if main_count < 40:
            return None, invalid_cards, (
                "O deck gerado ficou com menos de 40 cartas no main deck após a validação."
            )

        if extra_count > 15:
            return None, invalid_cards, (
                "O deck gerado ficou com mais de 15 cartas no extra deck após a validação."
            )

        if side_count > 15:
            return None, invalid_cards, (
                "O deck gerado ficou com mais de 15 cartas no side deck após a validação."
            )

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

        if invalid_cards:
            message = (
                "Deck salvo com sucesso, mas algumas cartas sugeridas pela IA não foram encontradas no catálogo."
            )

        return (ChatSavedDeckSummary(
            id=saved_deck.id,
            name=saved_deck.name,
            archetype=saved_deck.archetype,
            play_style=saved_deck.play_style,
            format=saved_deck.format,
            source=saved_deck.source,
        ),
            invalid_cards,
            message,
        )
