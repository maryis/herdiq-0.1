import os
import aiohttp

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def call_llm(prompt: str) -> str:
    """Call Gemini 1.5 Flash (fast & inexpensive)."""
    async with aiohttp.ClientSession() as session:
        params = {"key": GEMINI_API_KEY}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with session.post(GEMINI_URL, params=params, json=payload) as r:
            data = await r.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                return f"[Gemini error] {data}"
