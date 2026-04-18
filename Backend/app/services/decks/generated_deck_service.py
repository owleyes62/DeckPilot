from app.repositories.card_repository import CardRepository
from app.schemas.card import CardResponse
from app.schemas.chat import (ChatGeneratedDeck, ChatSavedDeckCard,
                              ChatSavedDeckDetail, ChatSavedDeckSummary)
from app.schemas.deck import DeckCreate
from app.schemas.deck_card import DeckCardCreate
from app.services.cards.card_import_service import CardImportService
from app.services.decks.archetype_core_service import ArchetypeCoreService
from app.services.decks.deck_service import DeckService
from sqlalchemy.ext.asyncio import AsyncSession


class GeneratedDeckService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.card_repository = CardRepository(db)
        self.deck_service = DeckService(db)
        self.archetype_core_service = ArchetypeCoreService()
        self.card_import_service = CardImportService(db)

    async def _find_or_import_card(self, card_name: str):
        existing_card = await self.card_repository.get_by_name(card_name)
        if existing_card:
            return existing_card

        json_entry = self.card_import_service.find_card_in_json_by_name(
            card_name)
        if json_entry:
            return await self.card_import_service.import_card_from_json_entry(json_entry)

        return None

    async def _merge_with_archetype_core(
        self,
        generated_deck: ChatGeneratedDeck,
    ) -> list[tuple[str, int, str]]:
        merged: dict[tuple[str, str], int] = {}

        for item in generated_deck.cards:
            key = (item.name, item.section)
            merged[key] = max(merged.get(key, 0), item.copies)

        core_cards = self.archetype_core_service.get_core(
            generated_deck.archetype)

        for core_card in core_cards:
            key = (core_card.name, core_card.section)
            if key not in merged:
                merged[key] = core_card.copies

        return [(name, copies, section) for (name, section), copies in merged.items()]

    async def validate_and_save_generated_deck(
        self,
        generated_deck: ChatGeneratedDeck,
    ) -> tuple[ChatSavedDeckSummary | None, ChatSavedDeckDetail | None, list[str], str]:
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
            return None, None, invalid_cards, "Nenhuma carta gerada foi encontrada no catálogo local."

        extra_count = sum(
            card.copies for card in valid_cards if card.section == "extra")
        side_count = sum(
            card.copies for card in valid_cards if card.section == "side")

        if extra_count > 15:
            return None, None, invalid_cards, (
                "O deck gerado ficou com mais de 15 cartas no extra deck após a validação."
            )

        if side_count > 15:
            return None, None, invalid_cards, (
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
        saved_deck_full = await self.deck_service.get_deck_by_id(saved_deck.id)

        message = "Deck gerado e salvo com sucesso."
        if invalid_cards:
            message = (
                "Deck salvo com sucesso, mas algumas cartas sugeridas pela IA não foram encontradas no catálogo."
            )

        summary = ChatSavedDeckSummary(
            id=saved_deck.id,
            name=saved_deck.name,
            archetype=saved_deck.archetype,
            play_style=saved_deck.play_style,
            format=saved_deck.format,
            source=saved_deck.source,
        )

        detail = None
        if saved_deck_full:
            detail = ChatSavedDeckDetail(
                id=saved_deck_full.id,
                name=saved_deck_full.name,
                archetype=saved_deck_full.archetype,
                play_style=saved_deck_full.play_style,
                format=saved_deck_full.format,
                win_condition=saved_deck_full.win_condition,
                how_to_pilot=saved_deck_full.how_to_pilot,
                source=saved_deck_full.source,
                deck_cards=[
                    ChatSavedDeckCard(
                        copies=item.copies,
                        section=item.section,
                        card=CardResponse.model_validate(item.card),
                    )
                    for item in saved_deck_full.deck_cards
                ],
            )

        return summary, detail, invalid_cards, message
