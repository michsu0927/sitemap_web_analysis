from typing import List
import xml.etree.ElementTree as ET


def parse_bytes(data: bytes) -> List[str]:
    text = data.decode(errors='ignore')
    text = text.strip()
    if text.startswith('<'):
        try:
            root = ET.fromstring(text)
            return [elem.text for elem in root.findall('.//{*}loc') if elem.text]
        except ET.ParseError:
            pass
    return [line.strip() for line in text.splitlines() if line.strip()]
