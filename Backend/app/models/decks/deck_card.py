from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import (DateTime, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.cards.card import Card
    from app.models.decks.deck import Deck


class DeckCard(Base):
    __tablename__ = "deck_cards"
    __table_args__ = (
        UniqueConstraint("deck_id", "card_id", "section",
                         name="uq_deck_card_section"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey(
        "decks.id", ondelete="CASCADE"), nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey(
        "cards.id", ondelete="CASCADE"), nullable=False)

    copies: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[str] = mapped_column(String(20), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deck: Mapped["Deck"] = relationship("Deck", back_populates="deck_cards")
    card: Mapped["Card"] = relationship("Card", back_populates="deck_cards")
