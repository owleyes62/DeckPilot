from collections import defaultdict

from app.schemas.deck import DeckCreate
from app.schemas.deck_validation import (DeckValidationIssue,
                                         DeckValidationResponse,
                                         DeckValidationSummary)


class DeckValidationService:
    def validate(self, payload: DeckCreate) -> DeckValidationResponse:
        issues: list[DeckValidationIssue] = []

        main_count = sum(
            card.copies for card in payload.cards if card.section == "main")
        extra_count = sum(
            card.copies for card in payload.cards if card.section == "extra")
        side_count = sum(
            card.copies for card in payload.cards if card.section == "side")
        total_count = main_count + extra_count + side_count

        if main_count < 40:
            issues.append(
                DeckValidationIssue(
                    code="MAIN_DECK_TOO_SMALL",
                    message="Main deck must contain at least 40 cards.",
                    section="main",
                )
            )

        if main_count > 60:
            issues.append(
                DeckValidationIssue(
                    code="MAIN_DECK_TOO_LARGE",
                    message="Main deck cannot contain more than 60 cards.",
                    section="main",
                )
            )

        if extra_count > 15:
            issues.append(
                DeckValidationIssue(
                    code="EXTRA_DECK_TOO_LARGE",
                    message="Extra deck cannot contain more than 15 cards.",
                    section="extra",
                )
            )

        if side_count > 15:
            issues.append(
                DeckValidationIssue(
                    code="SIDE_DECK_TOO_LARGE",
                    message="Side deck cannot contain more than 15 cards.",
                    section="side",
                )
            )

        duplicates: dict[tuple[str, str], int] = defaultdict(int)

        for card in payload.cards:
            key = (card.section, card.name.strip().lower())
            duplicates[key] += card.copies

        for (section, normalized_name), total_copies in duplicates.items():
            if total_copies > 3:
                issues.append(
                    DeckValidationIssue(
                        code="TOO_MANY_COPIES",
                        message="A card cannot have more than 3 copies in the same section.",
                        section=section,
                        card_name=normalized_name,
                    )
                )

        summary = DeckValidationSummary(
            main_count=main_count,
            extra_count=extra_count,
            side_count=side_count,
            total_count=total_count,
        )

        return DeckValidationResponse(
            is_valid=len(issues) == 0,
            summary=summary,
            issues=issues,
        )
