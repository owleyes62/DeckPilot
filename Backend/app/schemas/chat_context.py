from pydantic import BaseModel


class ChatSessionContext(BaseModel):
    archetype: str | None = None
    play_style: str | None = None
    format: str | None = None
    goal: str | None = None
    difficulty: str | None = None
    budget: str | None = None

    last_intent: str | None = None
    last_reply_summary: str | None = None
    suggested_archetypes: list[str] = []

    notes: list[str] = []
