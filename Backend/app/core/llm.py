import os

from app.core.config import settings
from google import genai
from openai import OpenAI


def get_doctor_llm_client():
    return OpenAI(
        api_key=settings.groq2_api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def get_chat_llm_client() -> OpenAI:
    return OpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
