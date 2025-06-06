from typing import List
import xml.etree.ElementTree as ET


def parse_bytes(data: bytes) -> List[str]:
    text = data.decode('utf-8', errors='replace') # Or 'backslashreplace' to see bad chars
    text = text.strip()
    if text.startswith('<'):
        try:
            root = ET.fromstring(text)
            return [elem.text for elem in root.findall('.//{*}loc') if elem.text]
        except ET.ParseError as e:
            # import logging
            # logging.warning(f"Failed to parse XML, falling back to line-by-line parsing: {e}")
            pass
    return [line.strip() for line in text.splitlines() if line.strip()]
