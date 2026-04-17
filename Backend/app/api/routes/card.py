from app.core.database import get_db
from app.schemas.card import CardListResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.app.services.cards.card_import_service import CardImportService
from Backend.app.services.chat.card_service import CardService

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.post("/import")
async def import_cards(
    db: AsyncSession = Depends(get_db),
):
    service = CardImportService(db)

    try:
        result = await service.import_from_file("data/ygojson/cards.json")
        return {
            "message": "Cards imported successfully",
            "result": result,
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("", response_model=list[CardListResponse])
async def list_cards(
    db: AsyncSession = Depends(get_db),
):
    service = CardService(db)
    return await service.list_cards()


@router.get("/search", response_model=list[CardListResponse])
async def search_cards(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = CardService(db)
    return await service.search_cards(query=q, limit=limit)
