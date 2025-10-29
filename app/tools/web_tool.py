import os, aiohttp, asyncio
from bs4 import BeautifulSoup
from google.cloud import storage
import datetime

BUCKET_NAME = os.getenv("CACHE_BUCKET")
SITES = [
    "https://yoursite1.com",
    "https://yoursite2.com",
]

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as r:
            html = await r.text()
            soup = BeautifulSoup(html, "html.parser")
            return " ".join(soup.stripped_strings)[:4000]

def _storage_client():
    return storage.Client()

def _cache_key(url): return f"site_cache/{hash(url)}.txt"

def read_from_cache(url):
    client = _storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(_cache_key(url))
    if blob.exists():
        age = datetime.datetime.now(datetime.timezone.utc) - blob.updated
        if age.days < 1:   # refresh daily
            return blob.download_as_text()
    return None

def write_to_cache(url, text):
    client = _storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(_cache_key(url))
    blob.upload_from_string(text)

async def fetch_context(query: str):
    """Fetch from cache or refresh if stale."""
    texts = []
    for url in SITES:
        cached = read_from_cache(url)
        if cached:
            texts.append(cached)
        else:
            try:
                html = await fetch_html(url)
                write_to_cache(url, html)
                texts.append(html)
            except Exception as e:
                texts.append(f"[Fetch error {url}: {e}]")
    return " ".join(texts)
