from app.api.routes import card, chat, deck, doctor, health
from fastapi import FastAPI

app = FastAPI(
    title="DeckPilot API",
    description="Your AI-powered Yu-Gi-Oh! deckbuilding copilot.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(deck.router)
app.include_router(card.router)
app.include_router(doctor.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "message": "DeckPilot API is running"
    }
