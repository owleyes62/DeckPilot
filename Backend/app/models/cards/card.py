from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from Backend.app.models.decks.deck_card import DeckCard


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int | None] = mapped_column(
        Integer, unique=True, nullable=True, index=True)
    name: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True)
    card_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    race: Mapped[str | None] = mapped_column(String(100), nullable=True)
    attribute: Mapped[str | None] = mapped_column(String(50), nullable=True)
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    atk: Mapped[int | None] = mapped_column(Integer, nullable=True)
    defense: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_small_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_cropped_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped[str] = mapped_column(
        String(30), nullable=False, default="ygojson")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deck_cards: Mapped[list["DeckCard"]] = relationship(
        "DeckCard",
        back_populates="card",
    )
