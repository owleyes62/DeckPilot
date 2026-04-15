from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeckCreate(BaseModel):
    archetype: str
    play_style: str
    deck_json: str
    win_condition: str | None = None
    how_to_pilot: str | None = None


class DeckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    archetype: str
    play_style: str
    deck_json: str
    win_condition: str | None = None
    how_to_pilot: str | None = None
    created_at: datetime
