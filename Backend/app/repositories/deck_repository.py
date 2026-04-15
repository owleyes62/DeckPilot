from app.models.card import Card
from app.models.deck import Deck
from app.models.deck_card import DeckCard
from app.schemas.deck import DeckCreate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class DeckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_card_by_name(self, name: str) -> Card | None:
        normalized_name = name.strip().lower()
        result = await self.db.execute(
            select(Card).where(func.lower(Card.name) == normalized_name)
        )
        return result.scalar_one_or_none()

    async def create(self, payload: DeckCreate) -> Deck:
        deck = Deck(
            name=payload.name,
            archetype=payload.archetype,
            play_style=payload.play_style,
            format=payload.format,
            win_condition=payload.win_condition,
            how_to_pilot=payload.how_to_pilot,
            source=payload.source,
        )

        self.db.add(deck)
        await self.db.flush()

        for item in payload.cards:
            card = await self._get_card_by_name(item.name)

            if not card:
                card = Card(
                    name=item.name.strip(),
                    external_id=item.external_id,
                    card_type=item.card_type,
                    race=item.race,
                    attribute=item.attribute,
                    level=item.level,
                    atk=item.atk,
                    defense=item.defense,
                    description=item.description,
                    image_url=item.image_url,
                    image_small_url=item.image_small_url,
                    image_cropped_url=item.image_cropped_url,
                    source=item.source,
                )
                self.db.add(card)
                await self.db.flush()

            deck_card = DeckCard(
                deck_id=deck.id,
                card_id=card.id,
                copies=item.copies,
                section=item.section,
            )
            self.db.add(deck_card)

        await self.db.commit()

        result = await self.db.execute(
            select(Deck)
            .options(
                selectinload(Deck.deck_cards).selectinload(DeckCard.card)
            )
            .where(Deck.id == deck.id)
        )
        return result.scalar_one()

    async def list_all(self) -> list[Deck]:
        result = await self.db.execute(
            select(Deck).order_by(Deck.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, deck_id: int) -> Deck | None:
        result = await self.db.execute(
            select(Deck)
            .options(
                selectinload(Deck.deck_cards).selectinload(DeckCard.card)
            )
            .where(Deck.id == deck_id)
        )
        return result.scalar_one_or_none()
