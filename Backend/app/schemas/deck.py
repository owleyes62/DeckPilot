from datetime import datetime

from app.schemas.deck_card import DeckCardCreate, DeckCardResponse
from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)


class DeckCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    archetype: str = Field(..., min_length=1, max_length=100)
    play_style: str = Field(..., min_length=1, max_length=50)
    format: str = Field(default="TCG", min_length=1, max_length=50)
    win_condition: str | None = None
    how_to_pilot: str | None = None
    source: str = "generated"
    cards: list[DeckCardCreate]

    @field_validator("name", "archetype", "play_style", "format", "source")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value

    @field_validator("source")
    @classmethod
    def normalize_source(cls, value: str) -> str:
        return value.lower()

    @model_validator(mode="after")
    def validate_cards(self):
        if not self.cards:
            raise ValueError("Deck must contain at least one card.")

        main_count = sum(
            card.copies for card in self.cards if card.section == "main")
        extra_count = sum(
            card.copies for card in self.cards if card.section == "extra")
        side_count = sum(
            card.copies for card in self.cards if card.section == "side")

        if main_count > 60:
            raise ValueError("Main deck cannot have more than 60 cards.")

        if extra_count > 15:
            raise ValueError("Extra deck cannot have more than 15 cards.")

        if side_count > 15:
            raise ValueError("Side deck cannot have more than 15 cards.")

        return self


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
