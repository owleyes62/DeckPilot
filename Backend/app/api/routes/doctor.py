from app.core.database import get_db
from app.schemas.deck_doctor import DeckDoctorAnalysisResponse
from app.schemas.deck_doctor_ai import DeckDoctorAIResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.app.services.ai.deck_doctor_ai_service import DeckDoctorAIService
from Backend.app.services.decks.deck_doctor_service import DeckDoctorService
from Backend.app.services.decks.deck_service import DeckService

router = APIRouter(prefix="/doctor", tags=["Deck Doctor"])


@router.get("/decks/{deck_id}", response_model=DeckDoctorAnalysisResponse)
async def analyze_deck(
    deck_id: int,
    db: AsyncSession = Depends(get_db),
):
    deck_service = DeckService(db)
    deck = await deck_service.get_deck_by_id(deck_id)

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    doctor_service = DeckDoctorService()
    return doctor_service.analyze(deck)


@router.get("/decks/{deck_id}/ai", response_model=DeckDoctorAIResponse)
async def analyze_deck_with_ai(
    deck_id: int,
    db: AsyncSession = Depends(get_db),
):
    deck_service = DeckService(db)
    deck = await deck_service.get_deck_by_id(deck_id)

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    doctor_service = DeckDoctorService()
    structural_analysis = doctor_service.analyze(deck)

    ai_service = DeckDoctorAIService()
    return ai_service.analyze_with_ai(deck=deck, analysis=structural_analysis)
