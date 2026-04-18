import json

from app.core.config import settings
from app.core.llm import get_doctor_llm_client
from app.core.prompt_loader import load_prompt
from app.models.decks.deck import Deck
from app.schemas.deck_doctor import DeckDoctorAnalysisResponse
from app.schemas.deck_doctor_ai import DeckDoctorAIResponse


class DeckDoctorAIService:
    def _build_structured_input(
        self,
        deck: Deck,
        analysis: DeckDoctorAnalysisResponse,
    ) -> str:
        deck_cards = [
            {
                "name": item.card.name,
                "section": item.section,
                "copies": item.copies,
                "card_type": item.card.card_type,
            }
            for item in deck.deck_cards
        ]

        payload = {
            "deck": {
                "id": deck.id,
                "name": deck.name,
                "archetype": deck.archetype,
                "play_style": deck.play_style,
                "format": deck.format,
                "win_condition": deck.win_condition,
                "how_to_pilot": deck.how_to_pilot,
            },
            "analysis": analysis.model_dump(),
            "cards": deck_cards,
        }

        return json.dumps(payload, ensure_ascii=False, indent=2)

    def analyze_with_ai(
        self,
        deck: Deck,
        analysis: DeckDoctorAnalysisResponse,
    ) -> DeckDoctorAIResponse:
        client = get_doctor_llm_client()

        system_prompt = load_prompt("deck_doctor/system.txt")
        user_template = load_prompt("deck_doctor/user_template.txt")

        structured_input = self._build_structured_input(
            deck=deck, analysis=analysis)
        user_prompt = user_template.format(structured_input=structured_input)

        response = client.chat.completions.create(
            model=settings.llm2_model,
            temperature=0.4,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)

        return DeckDoctorAIResponse(
            deck_id=deck.id,
            summary=parsed.get("summary", ""),
            strengths=parsed.get("strengths", []),
            risks=parsed.get("risks", []),
            suggestions=parsed.get("suggestions", []),
        )
