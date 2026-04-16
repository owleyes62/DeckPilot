from app.services.card_catalog_service import CardCatalogService
from sqlalchemy.ext.asyncio import AsyncSession


class ChatToolService:
    def __init__(self, db: AsyncSession):
        self.card_catalog_service = CardCatalogService(db)

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        if tool_name == "search_cards":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 20)
            results = await self.card_catalog_service.search_cards(query=query, limit=limit)
            return {"tool_name": tool_name, "results": results}

        if tool_name == "get_cards_by_names":
            names = arguments.get("names", [])
            results = await self.card_catalog_service.get_cards_by_names(names=names)
            return {"tool_name": tool_name, "results": results}

        if tool_name == "get_archetype_candidates":
            archetype = arguments.get("archetype", "")
            limit = arguments.get("limit", 30)
            results = await self.card_catalog_service.get_archetype_candidates(
                archetype=archetype,
                limit=limit,
            )
            return {"tool_name": tool_name, "results": results}

        if tool_name == "discover_cards_for_preferences":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 30)
            results = await self.card_catalog_service.discover_cards_for_preferences(
                query=query,
                limit=limit,
            )
            return {"tool_name": tool_name, "results": results}

        raise ValueError(f"Unknown tool: {tool_name}")
