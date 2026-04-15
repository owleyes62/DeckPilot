from app.api.routes import health
from fastapi import FastAPI

app = FastAPI(
    title="DeckPilot API",
    description="Your AI-powered Yu-Gi-Oh! deckbuilding copilot.",
    version="0.1.0",
)

app.include_router(health.router)


@app.get("/")
def root():
    return {
        "message": "DeckPilot API is running"
    }
