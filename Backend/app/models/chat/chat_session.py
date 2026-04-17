from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from Backend.app.models.chat.chat_generated_deck import ChatGeneratedDeck
    from Backend.app.models.chat.chat_message import ChatMessage


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(
        String(150), nullable=False, default="Nova conversa")

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

    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.id",
    )

    generated_decks: Mapped[list["ChatGeneratedDeck"]] = relationship(
        "ChatGeneratedDeck",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatGeneratedDeck.generation_index",
    )
