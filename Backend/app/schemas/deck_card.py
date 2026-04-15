from typing import Literal

from app.schemas.card import CardResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeckCardCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    copies: int = Field(..., ge=1, le=3)
    section: Literal["main", "extra", "side"]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Card name cannot be empty.")
        return value


class DeckCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    copies: int
    section: str
    card: CardResponse
