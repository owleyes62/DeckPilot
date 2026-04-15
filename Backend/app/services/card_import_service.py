import json
from pathlib import Path
from typing import Any

from app.repositories.card_repository import CardRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CardImportService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = CardRepository(db)

    def _extract_card_payload(self, raw_card: dict[str, Any]) -> dict[str, Any]:
        card_images = raw_card.get("card_images", [])
        first_image = card_images[0] if card_images else {}

        return {
            "external_id": raw_card.get("id"),
            "name": raw_card.get("name"),
            "card_type": raw_card.get("type"),
            "race": raw_card.get("race"),
            "attribute": raw_card.get("attribute"),
            "level": raw_card.get("level"),
            "atk": raw_card.get("atk"),
            "defense": raw_card.get("def"),
            "description": raw_card.get("desc"),
            "image_url": first_image.get("image_url"),
            "image_small_url": first_image.get("image_url_small"),
            "image_cropped_url": first_image.get("image_url_cropped"),
            "source": "ygojson",
        }

    async def import_from_file(self, file_path: str) -> dict[str, int]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        raw_cards = data.get("data", data)

        created = 0
        skipped = 0

        for raw_card in raw_cards:
            external_id = raw_card.get("id")
            name = raw_card.get("name")

            if not name:
                skipped += 1
                continue

            existing = None
            if external_id:
                existing = await self.repository.get_by_external_id(external_id)

            if not existing:
                existing = await self.repository.get_by_name(name)

            if existing:
                skipped += 1
                continue

            payload = self._extract_card_payload(raw_card)
            await self.repository.create(**payload)
            created += 1

        await self.db.commit()

        return {
            "created": created,
            "skipped": skipped,
            "total": len(raw_cards),
        }
