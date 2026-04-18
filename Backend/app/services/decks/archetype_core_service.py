import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArchetypeCoreCard:
    name: str
    copies: int
    section: str = "main"


class ArchetypeCoreService:
    def __init__(self):
        self.data_path = Path("data/archetype/archetype_cores.json")
        self.aliases = {
            "despia branded": "branded",
            "branded despia": "branded",
            "traptrix": "traptrix",
            "swordsoul": "swordsoul",
            "sword soul": "swordsoul",
        }

    def _load_cores(self) -> dict[str, list[dict]]:
        if not self.data_path.exists():
            return {}

        with self.data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def normalize_archetype(self, archetype: str | None) -> str | None:
        if not archetype:
            return None

        normalized = archetype.lower().strip()
        return self.aliases.get(normalized, normalized)

    def get_core(self, archetype: str | None) -> list[ArchetypeCoreCard]:
        normalized = self.normalize_archetype(archetype)
        if not normalized:
            return []

        raw_cores = self._load_cores()
        raw_cards = raw_cores.get(normalized, [])

        return [
            ArchetypeCoreCard(
                name=item["name"],
                copies=item["copies"],
                section=item.get("section", "main"),
            )
            for item in raw_cards
        ]
