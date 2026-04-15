from app.core.database import get_db
from app.schemas.deck import DeckCreate, DeckListResponse, DeckResponse
from app.schemas.deck_validation import DeckValidationResponse
from app.services.deck_service import DeckService
from app.services.deck_validation_service import DeckValidationService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.post("", response_model=DeckResponse, status_code=201)
async def create_deck(
    payload: DeckCreate,
    db: AsyncSession = Depends(get_db),
):
    service = DeckService(db)
    return await service.create_deck(payload)


@router.get("", response_model=list[DeckListResponse])
async def list_decks(
    db: AsyncSession = Depends(get_db),
):
    service = DeckService(db)
    return await service.list_decks()


@router.get("/{deck_id}", response_model=DeckResponse)
async def get_deck(
    deck_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = DeckService(db)
    deck = await service.get_deck_by_id(deck_id)

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    return deck


@router.post("/validate", response_model=DeckValidationResponse)
async def validate_deck(
    payload: DeckCreate,
):
    service = DeckValidationService()
    return service.validate(payload)
