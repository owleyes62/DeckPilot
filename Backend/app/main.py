from app.api.routes import card, chat, deck, doctor, health
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DeckPilot API",
    description="Your AI-powered Yu-Gi-Oh! deckbuilding copilot.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
