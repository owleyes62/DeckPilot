from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatSessionCreate(BaseModel):
    title: str | None = None


class ChatSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message content cannot be empty.")
        return value


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime


class ChatSuggestedArchetype(BaseModel):
    name: str
    reason: str


class ChatDeckRequest(BaseModel):
    archetype: str | None = None
    play_style: str | None = None
    format: str | None = None
    goal: str | None = None
    difficulty: str | None = None
    budget: str | None = None


class ChatGeneratedDeckCard(BaseModel):
    name: str
    copies: int
    section: Literal["main", "extra", "side"]


class ChatGeneratedDeck(BaseModel):
    name: str
    archetype: str
    play_style: str
    format: str
    win_condition: str
    how_to_pilot: str
    cards: list[ChatGeneratedDeckCard]


class ChatAIResponse(BaseModel):
    reply: str
    intent: Literal[
        "known_deck_request",
        "deck_discovery_request",
        "refine_existing_deck",
        "general_chat",
    ]
    should_ask_questions: bool
    questions: list[str]
    suggested_archetypes: list[ChatSuggestedArchetype]
    deck_request: ChatDeckRequest | None = None
    generated_deck: ChatGeneratedDeck | None = None


class ChatMessageExchangeResponse(BaseModel):
    session_id: int
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
    ai_response: ChatAIResponse
