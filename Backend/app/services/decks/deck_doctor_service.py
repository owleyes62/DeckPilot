from app.schemas.deck_doctor import (DeckDoctorAnalysisResponse,
                                     DeckDoctorCounts, DeckDoctorIssue)

from Backend.app.models.decks.deck import Deck


class DeckDoctorService:
    def analyze(self, deck: Deck) -> DeckDoctorAnalysisResponse:
        main_cards = [
            item for item in deck.deck_cards if item.section == "main"]
        extra_cards = [
            item for item in deck.deck_cards if item.section == "extra"]
        side_cards = [
            item for item in deck.deck_cards if item.section == "side"]

        main_count = sum(item.copies for item in main_cards)
        extra_count = sum(item.copies for item in extra_cards)
        side_count = sum(item.copies for item in side_cards)
        total_count = main_count + extra_count + side_count

        monster_count = 0
        spell_count = 0
        trap_count = 0

        for item in main_cards:
            card_type = (item.card.card_type or "").lower()

            if "monster" in card_type:
                monster_count += item.copies
            elif "spell" in card_type:
                spell_count += item.copies
            elif "trap" in card_type:
                trap_count += item.copies

        issues: list[DeckDoctorIssue] = []
        recommendations: list[str] = []

        if main_count < 40:
            issues.append(
                DeckDoctorIssue(
                    code="MAIN_TOO_SMALL",
                    message="Main deck has fewer than 40 cards.",
                    severity="high",
                )
            )

        if main_count > 60:
            issues.append(
                DeckDoctorIssue(
                    code="MAIN_TOO_LARGE",
                    message="Main deck has more than 60 cards.",
                    severity="high",
                )
            )

        if extra_count > 15:
            issues.append(
                DeckDoctorIssue(
                    code="EXTRA_TOO_LARGE",
                    message="Extra deck has more than 15 cards.",
                    severity="high",
                )
            )

        if side_count > 15:
            issues.append(
                DeckDoctorIssue(
                    code="SIDE_TOO_LARGE",
                    message="Side deck has more than 15 cards.",
                    severity="high",
                )
            )

        if monster_count == 0:
            issues.append(
                DeckDoctorIssue(
                    code="NO_MONSTERS",
                    message="Main deck has no monsters.",
                    severity="medium",
                )
            )

        if main_count >= 40 and monster_count < 10:
            recommendations.append(
                "Consider increasing the number of monsters in the main deck.")

        if spell_count == 0:
            recommendations.append(
                "Consider adding spell cards for consistency or utility.")

        if trap_count == 0:
            recommendations.append(
                "Consider whether the strategy benefits from any trap interaction.")

        return DeckDoctorAnalysisResponse(
            deck_id=deck.id,
            counts=DeckDoctorCounts(
                main_count=main_count,
                extra_count=extra_count,
                side_count=side_count,
                total_count=total_count,
                monster_count=monster_count,
                spell_count=spell_count,
                trap_count=trap_count,
            ),
            issues=issues,
            recommendations=recommendations,
        )
