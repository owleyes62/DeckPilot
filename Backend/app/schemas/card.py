from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    name: str
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


class CardCreate(CardBase):
    pass


class CardResponse(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CardListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    card_type: str | None = None
    race: str | None = None
    attribute: str | None = None
    image_small_url: str | None = None
