README.md for sitemap-analysis-tool

# 🗺️ Sitemap Analysis Tool

A website structure and SEO analyzer that accepts input from **Web frontend** or **CLI**. Each analysis task is assigned a UUID, and results are stored in HTML, JSON, and TXT formats for sharing, reporting, or programmatic use.

---

## 📦 Features

- Input via:
  - ✅ Frontend (paste URLs or upload sitemap.xml)
  - ✅ CLI (upload `.txt` file of URLs)
- Generates a unique UUID for each task
- Analyzes each page for:
  - HTTP status code
  - Title
  - Meta description
  - Content size
  - Depth from root
- Generates:
  - `report.html`
  - `report.json`
  - `urls.txt`
  - (for CLI) `input.txt`
- Maintains task index (`task_index.json`)
- Simple and extensible FastAPI + React architecture

---

## 📁 Project Structure

sitemap-analysis-tool/
├── backend/
│ ├── main.py
│ ├── analyzer.py
│ ├── utils/
│ │ ├── sitemap_parser.py
│ │ ├── report_writer.py
│ │ └── task_index.py
│ ├── templates/
│ │ └── report_template.html
│ └── reports/
│ └── <uuid>/
│ ├── report.html
│ ├── report.json
│ ├── urls.txt
│ └── input.txt (if CLI)
├── frontend/ (optional)
│ └── ...
├── README.md
└── requirements.txt

yaml
複製
編輯

---

## 🚀 Getting Started (Backend Only)

```bash
# 1. Clone this repo
git clone https://github.com/yourname/sitemap-analysis-tool.git
cd sitemap-analysis-tool/backend

# 2. Set up virtual env (optional)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload
```
🧠 API Overview
▶ POST /analyze
Frontend input (URLs or sitemap)
```
Body: multipart/form-data

urls (optional): pasted URLs (newline separated)

file (optional): sitemap.xml file

Returns: { "uuid": "<uuid>", "report_url": "/report/<uuid>" }
```
▶ POST /cli/analyze
CLI upload of .txt URL file
```
Form field: file=@urls.txt

Returns: { "uuid": "<uuid>", "report_url": "/report/<uuid>" }
```
▶ GET /report/<uuid>
Returns rendered HTML report for a task.

▶ GET /report/<uuid>/report.json
Returns raw JSON of analysis result.

▶ GET /report/<uuid>/urls.txt
Returns all successfully analyzed URLs as plain text.

▶ GET /report/list
Returns task_index.json, including all UUIDs and timestamps.

📄 Example CLI Upload
bash
複製
編輯
curl -X POST http://localhost:8000/cli/analyze \
  -F 'file=@urls.txt'
📂 Example Output (per task)
graphql
reports/
└── fc9b5aee/
    ├── report.html         # Final HTML report
    ├── report.json         # All result data (for API or front-end)
    ├── urls.txt            # Successfully analyzed URLs
    └── input.txt           # Original URL input (if CLI)
🧪 Analysis Data Format (report.json)
json
{
  "uuid": "fc9b5aee",
  "analyzed_at": "2025-06-06T10:25:00",
  "total_urls": 23,
  "successful": 21,
  "failed": 2,
  "pages": [
    {
      "url": "https://example.com/",
      "status_code": 200,
      "title": "Home",
      "meta_description": "Welcome!",
      "depth": 0,
      "size": 10458
    }
  ]
}
🗃 Task Index (task_index.json)
[
  { "uuid": "fc9b5aee", "created_at": "2025-06-06T10:25:00" },
  { "uuid": "bdc82210", "created_at": "2025-06-06T11:09:13" }
]
🧰 Developer Notes
All report files are written to backend/reports/<uuid>/

task_index.json is auto-updated for each new task

UUIDs are 8-char lowercase (uuid4().hex[:8])

✅ TODO / Future Features
 Sitemap index parsing

 Progress API for live updates

 Graph visualization of page structure

 User login and private task tracking

📃 License
MIT License © 2025 Mic Hsu & Contributors
