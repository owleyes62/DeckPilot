from datetime import datetime
from typing import Any, Literal

from app.schemas.card import CardResponse
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


class ChatToolCallResponse(BaseModel):
    type: str
    tool_name: str
    arguments: dict[str, Any]


class ChatFinalAnswerResponse(BaseModel):
    type: str
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


class ChatSavedDeckSummary(BaseModel):
    id: int
    name: str
    archetype: str
    play_style: str
    format: str
    source: str


class ChatGenerationStatus(BaseModel):
    attempted: bool
    saved: bool
    message: str


class ChatSavedDeckCard(BaseModel):
    copies: int
    section: str
    card: CardResponse


class ChatSavedDeckDetail(BaseModel):
    id: int
    name: str
    archetype: str
    play_style: str
    format: str
    win_condition: str | None = None
    how_to_pilot: str | None = None
    source: str
    deck_cards: list[ChatSavedDeckCard]


class ChatMessageExchangeResponse(BaseModel):
    session_id: int
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
    ai_response: ChatFinalAnswerResponse
    saved_deck: ChatSavedDeckSummary | None = None
    saved_deck_detail: ChatSavedDeckDetail | None = None
    invalid_cards: list[str] = []
    generation_status: ChatGenerationStatus
