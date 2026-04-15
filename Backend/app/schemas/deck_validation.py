from pydantic import BaseModel


class DeckValidationIssue(BaseModel):
    code: str
    message: str
    section: str | None = None
    card_name: str | None = None


class DeckValidationSummary(BaseModel):
    main_count: int
    extra_count: int
    side_count: int
    total_count: int


class DeckValidationResponse(BaseModel):
    is_valid: bool
    summary: DeckValidationSummary
    issues: list[DeckValidationIssue]
