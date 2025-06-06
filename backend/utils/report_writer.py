from pathlib import Path
from typing import List, Dict, Optional
import json
import html

TEMPLATE = """<html><head><title>Report {uid}</title></head><body><h1>Report {uid}</h1><pre>{data}</pre></body></html>"""


def write_report(base: Path, uid: str, results: List[Dict], urls: List[str], input_txt: Optional[str] = None) -> Path:
    task_dir = base / uid
    task_dir.mkdir(exist_ok=True)

    (task_dir / "report.json").write_text(json.dumps(results, indent=2))
    (task_dir / "urls.txt").write_text("\n".join(urls))
    if input_txt:
        (task_dir / "input.txt").write_text(input_txt)

    html_content = TEMPLATE.format(uid=uid, data=html.escape(json.dumps(results, indent=2)))
    (task_dir / "report.html").write_text(html_content)

    return task_dir
