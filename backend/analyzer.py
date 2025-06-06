import asyncio
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup

async def fetch(session: httpx.AsyncClient, url: str) -> Dict:
    try:
        resp = await session.get(url, timeout=10)
        status = resp.status_code
        content = resp.text
    except Exception:
        return {"url": url, "status_code": None, "error": "fetch_failed"}

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string.strip() if soup.title else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    description = meta['content'].strip() if meta and meta.has_attr('content') else ''
    size = len(content.encode('utf-8'))

    return {
        "url": url,
        "status_code": status,
        "title": title,
        "meta_description": description,
        "size": size,
    }

async def analyze_urls(urls: List[str]) -> List[Dict]:
    results: List[Dict] = []
async def analyze_urls(session: httpx.AsyncClient, urls: List[str]) -> List[Dict]:
    results: List[Dict] = []
    tasks = [fetch(session, url) for url in urls]
    for coro in asyncio.as_completed(tasks):
        results.append(await coro)
    return results
