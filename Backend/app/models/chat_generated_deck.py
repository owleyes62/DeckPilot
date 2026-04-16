from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.chat_session import ChatSession
    from app.models.deck import Deck


class ChatGeneratedDeck(Base):
    __tablename__ = "chat_generated_decks"
    __table_args__ = (
        UniqueConstraint("session_id", "generation_index",
                         name="uq_chat_generation_index"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deck_id: Mapped[int] = mapped_column(
        ForeignKey("decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    generation_index: Mapped[int] = mapped_column(Integer, nullable=False)

    user_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="SET NULL"),
        nullable=True,
    )
    assistant_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped["ChatSession"] = relationship(
        "ChatSession", back_populates="generated_decks")
    deck: Mapped["Deck"] = relationship(
        "Deck", back_populates="chat_generated_links")
