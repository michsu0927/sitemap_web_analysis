import asyncio
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup

from . import llm_analyzer

async def fetch(session: httpx.AsyncClient, url: str) -> Dict:
    try:
        resp = await session.get(url, timeout=10)
        status = resp.status_code
        content = resp.text
    except httpx.RequestError:
        return {"url": url, "status_code": None, "error": "fetch_failed"}

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string.strip() if soup.title else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    description = meta['content'].strip() if meta and meta.has_attr('content') else ''
    size = len(content.encode('utf-8'))

    result: Dict[str, Optional[str]] = {
        "url": url,
        "status_code": status,
        "title": title,
        "meta_description": description,
        "size": size,
    }

    if llm_analyzer.is_configured():
        analysis = await llm_analyzer.analyze_text(content)
        if analysis:
            result["llm_analysis"] = analysis

    return result

async def analyze_urls(urls: List[str]) -> List[Dict]:
    results: List[Dict] = []
    async with httpx.AsyncClient(follow_redirects=True) as session:
        tasks = [fetch(session, url) for url in urls]
        for coro in asyncio.as_completed(tasks):
            results.append(await coro)
    return results
