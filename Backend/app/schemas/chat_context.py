from pydantic import BaseModel


class ChatSessionContext(BaseModel):
    archetype: str | None = None
    play_style: str | None = None
    format: str | None = None
    goal: str | None = None
    difficulty: str | None = None
    budget: str | None = None
    notes: list[str] = []
