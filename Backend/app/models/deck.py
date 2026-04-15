from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.deck_card import DeckCard
    from app.models.deck_diagnosis import DeckDiagnosis
    from app.models.simulation_run import SimulationRun


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    archetype: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True)
    play_style: Mapped[str] = mapped_column(String(50), nullable=False)
    format: Mapped[str] = mapped_column(
        String(50), nullable=False, default="TCG")
    win_condition: Mapped[str | None] = mapped_column(Text, nullable=True)
    how_to_pilot: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(
        String(30), nullable=False, default="generated")

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
        back_populates="deck",
        cascade="all, delete-orphan",
    )
    diagnoses: Mapped[list["DeckDiagnosis"]] = relationship(
        "DeckDiagnosis",
        back_populates="deck",
        cascade="all, delete-orphan",
    )
    simulation_runs: Mapped[list["SimulationRun"]] = relationship(
        "SimulationRun",
        back_populates="deck",
        cascade="all, delete-orphan",
    )
