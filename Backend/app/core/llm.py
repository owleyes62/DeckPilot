from app.core.config import settings
from openai import OpenAI


def get_groq_client() -> OpenAI:
    return OpenAI(api_key=settings.groq_api_key,
                  base_url="https://api.groq.com/openai/v1",)
