from pydantic import BaseModel


class DeckDoctorCounts(BaseModel):
    main_count: int
    extra_count: int
    side_count: int
    total_count: int
    monster_count: int
    spell_count: int
    trap_count: int


class DeckDoctorIssue(BaseModel):
    code: str
    message: str
    severity: str


class DeckDoctorAnalysisResponse(BaseModel):
    deck_id: int
    counts: DeckDoctorCounts
    issues: list[DeckDoctorIssue]
    recommendations: list[str]
