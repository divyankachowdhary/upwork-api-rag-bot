
from __future__ import annotations

from pathlib import Path

import pdfplumber
from langchain_core.documents import Document


def _serialize_table(table: list[list[str | None]]) -> str:
    if not table or len(table) < 2:
        return ""

    headers = [(h or "").strip() for h in table[0]]
    lines: list[str] = []
    for row in table[1:]:
        cells = []
        for header, raw in zip(headers, row):
            value = (raw or "").strip()
            if not value:
                continue
            cells.append(f"{header}: {value}" if header else value)
        if cells:
            lines.append(" | ".join(cells))
    return "\n".join(lines)


def load_pdf(path: Path) -> list[Document]:
    if not path.exists():
        raise FileNotFoundError(f"Source PDF not found: {path}")

    source_name = f"{path.parent.name}/{path.name}" if path.parent.name else path.name
    documents: list[Document] = []
    with pdfplumber.open(str(path)) as pdf:
        for page_index, page in enumerate(pdf.pages):
            prose = page.extract_text() or ""

            table_blocks: list[str] = []
            for table in page.extract_tables() or []:
                serialized = _serialize_table(table)
                if serialized:
                    table_blocks.append(serialized)

            tables_text = ""
            if table_blocks:
                tables_text = "\n\n[TABLES]\n" + "\n\n".join(table_blocks)

            page_text = (prose + tables_text).strip()
            if not page_text:
                continue

            documents.append(
                Document(
                    page_content=page_text,
                    metadata={"source": source_name, "page": page_index},
                )
            )

    return documents
