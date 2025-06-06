from pathlib import Path
import json
def _index_file(base: Path) -> Path:
    return base / "task_index.json"

def read_index(base: Path):
    f = _index_file(base)
    if f.exists():
        return json.loads(f.read_text())
    return []

def add_task(base: Path, uid: str):
    idx = read_index(base)
    idx.append({"uuid": uid})
    _index_file(base).write_text(json.dumps(idx, indent=2))
