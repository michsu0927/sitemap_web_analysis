import asyncio
import os
from typing import Optional
from openai import AzureOpenAI

_client: Optional[AzureOpenAI] = None


def is_configured() -> bool:
    return bool(os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_DEPLOYMENT"))


def _get_client() -> Optional[AzureOpenAI]:
    global _client
    if _client is None and is_configured():
        _client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    return _client


async def analyze_text(text: str) -> Optional[str]:
    client = _get_client()
    if not client:
        return None
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    max_tokens = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "256"))
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            deployment_id=deployment,
            messages=[
                {"role": "system", "content": "You are an SEO analyzer."},
                {"role": "user", "content": text},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
