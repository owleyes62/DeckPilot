from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.decks.deck import Deck


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(ForeignKey(
        "decks.id", ondelete="CASCADE"), nullable=False)

    iterations: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10000)
    starter_probability: Mapped[float |
                                None] = mapped_column(Float, nullable=True)
    brick_probability: Mapped[float | None] = mapped_column(
        Float, nullable=True)
    playable_hand_probability: Mapped[float |
                                      None] = mapped_column(Float, nullable=True)

    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    llm_interpretation: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deck: Mapped["Deck"] = relationship(
        "Deck", back_populates="simulation_runs")
