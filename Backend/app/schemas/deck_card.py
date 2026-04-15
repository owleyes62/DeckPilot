from app.schemas.card import CardResponse
from pydantic import BaseModel, ConfigDict


class DeckCardCreate(BaseModel):
    name: str
    copies: int
    section: str
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


class DeckCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    copies: int
    section: str
    card: CardResponse
