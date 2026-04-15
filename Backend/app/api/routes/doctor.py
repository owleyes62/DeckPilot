from app.core.database import get_db
from app.schemas.deck_doctor import DeckDoctorAnalysisResponse
from app.services.deck_doctor_service import DeckDoctorService
from app.services.deck_service import DeckService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
