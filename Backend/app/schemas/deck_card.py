from typing import Literal

from app.schemas.card import CardResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeckCardCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    copies: int = Field(..., ge=1, le=3)
    section: Literal["main", "extra", "side"]
    external_id: int | None = None
    card_type: str | None = None
    race: str | None = None
    attribute: str | None = None
    level: int | None = None
    atk: int | None = None
    defense: int | None = None
    description: str | None = None
    image_url: str | None = None
    image_small_url: str | None = None
    image_cropped_url: str | None = None
    source: str = "ygojson"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Card name cannot be empty.")
        return value

    @field_validator("source")
    @classmethod
    def normalize_source(cls, value: str) -> str:
        return value.strip().lower()


class DeckCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    copies: int
    section: str
    card: CardResponse
