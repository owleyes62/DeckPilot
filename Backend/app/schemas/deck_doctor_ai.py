from pydantic import BaseModel


class DeckDoctorAIResponse(BaseModel):
    deck_id: int
    summary: str
    strengths: list[str]
    risks: list[str]
    suggestions: list[str]
