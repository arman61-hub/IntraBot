import re
from typing import Dict, List
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

from backend.app.rag.rbac import roles_for_department

MAX_TOKENS = 256
OVERLAP = 40


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _read_file(path: Path) -> str:
    if path.suffix == ".csv":
        return pd.read_csv(path).to_string(index=False)
    if path.suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def preprocess(directories: List[Path]) -> Dict:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    documents: List[Document] = []
    total_chunks = 0

    for directory in directories:
        for file in directory.rglob("*"):
            if file.suffix not in {".md", ".txt", ".csv"}:
                continue
            
            model.tokenizer.model_max_length = int(1e12)
            raw = _clean(_read_file(file))
            tokens = model.tokenizer.encode(raw, add_special_tokens=False)

            start = 0
            idx = 0

            while start < len(tokens):
                end = min(start + MAX_TOKENS, len(tokens))
                chunk_tokens = tokens[start:end]
                text = model.tokenizer.decode(chunk_tokens)

                roles = roles_for_department(directory.name)

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "chunk_id": f"{file}::chunk_{idx}",
                            "source_path": str(file),
                            "department": directory.name,
                            "accessible_roles": ",".join(roles),
                        },
                    )
                )

                total_chunks += 1
                idx += 1
                start = end - OVERLAP if end < len(tokens) else end

    return {
        "documents": documents,
        "total_documents": len(documents),
        "total_chunks": total_chunks,
    }


