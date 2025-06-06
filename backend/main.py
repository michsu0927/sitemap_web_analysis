from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from typing import List, Optional
from uuid import uuid4
from pathlib import Path
import json

from .analyzer import analyze_urls
from .utils import sitemap_parser, report_writer, task_index

app = FastAPI(title="Sitemap Analysis Tool")

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

@app.post("/analyze")
async def analyze(urls: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    if not urls and not file:
        raise HTTPException(status_code=400, detail="No input provided")

    url_list: List[str] = []
    if urls:
        url_list.extend([u.strip() for u in urls.splitlines() if u.strip()])
    if file:
        content = await file.read()
        url_list.extend(sitemap_parser.parse_bytes(content))

    if not url_list:
        raise HTTPException(status_code=400, detail="No URLs found")

    uid = uuid4().hex[:8]
    result = await analyze_urls(url_list)
    report_path = report_writer.write_report(REPORTS_DIR, uid, result, url_list)
    task_index.add_task(REPORTS_DIR, uid)

    return {"uuid": uid, "report_url": f"/report/{uid}"}

@app.post("/cli/analyze")
async def cli_analyze(file: UploadFile = File(...)):
    content = await file.read()
    url_list = sitemap_parser.parse_bytes(content)
    uid = uuid4().hex[:8]
    result = await analyze_urls(url_list)
    report_writer.write_report(REPORTS_DIR, uid, result, url_list, input_txt=content.decode())
    task_index.add_task(REPORTS_DIR, uid)
    return {"uuid": uid, "report_url": f"/report/{uid}"}

@app.get("/report/{uid}", response_class=HTMLResponse)
async def get_report(uid: str):
    report_file = REPORTS_DIR / uid / "report.html"
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return report_file.read_text()

@app.get("/report/{uid}/report.json")
async def get_report_json(uid: str):
    report_file = REPORTS_DIR / uid / "report.json"
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return JSONResponse(json.loads(report_file.read_text()))

@app.get("/report/{uid}/urls.txt")
async def get_urls(uid: str):
    urls_file = REPORTS_DIR / uid / "urls.txt"
    if not urls_file.exists():
        raise HTTPException(status_code=404, detail="URLs not found")
    return PlainTextResponse(report_file.read_text())

@app.get("/report/list")
async def list_reports():
    idx = task_index.read_index(REPORTS_DIR)
    return JSONResponse(idx)
