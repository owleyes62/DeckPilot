from datetime import datetime

from app.schemas.deck_card import DeckCardCreate, DeckCardResponse
from pydantic import BaseModel, ConfigDict


class DeckCreate(BaseModel):
    name: str
    archetype: str
    play_style: str
    format: str = "TCG"
    win_condition: str | None = None
    how_to_pilot: str | None = None
    source: str = "generated"
    cards: list[DeckCardCreate]


class DeckListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    archetype: str
    play_style: str
    format: str
    source: str
    created_at: datetime


class DeckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    archetype: str
    play_style: str
    format: str
    win_condition: str | None = None
    how_to_pilot: str | None = None
    source: str
    created_at: datetime
    updated_at: datetime
    deck_cards: list[DeckCardResponse]
