from __future__ import annotations

from csv import DictReader
from pathlib import Path


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    path = Path(path)
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        reader = DictReader(file)
        return list(reader)
