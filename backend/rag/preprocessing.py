import re
from typing import Dict, List
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

from backend.rag.rbac import roles_for_department

# ✅ FIXED: Set to 256 to match the AI model's limit. 
# This ensures NO data is ignored.
MAX_TOKENS = 256  
OVERLAP = 50      

def _clean(text: str) -> str:
    # Remove excessive formatting to save tokens
    text = re.sub(r"[-_]{3,}", " ", text)
    text = re.sub(r"(?:-\s*){5,}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def _read_file(path: Path) -> str:
    if path.suffix == ".csv":
        # Compact CSV format
        return pd.read_csv(path).to_string(index=False)
    if path.suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""

def preprocess(directories: List[Path]) -> Dict:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    tokenizer = model.tokenizer

    documents: List[Document] = []
    total_chunks = 0
    chunks_per_department: Dict[str, int] = {}

    for directory in directories:
        department = directory.name.lower()
        chunks_per_department.setdefault(department, 0)

        for file in directory.rglob("*"):
            if file.suffix not in {".md", ".txt", ".csv"}:
                continue

            raw = _clean(_read_file(file))
            if not raw:
                continue

            # Tokenize the entire file first
            token_ids = tokenizer(
                raw,
                add_special_tokens=False,
                truncation=False,
                return_attention_mask=False,
            )["input_ids"]

            start = 0
            idx = 0

            # Create overlapping chunks
            while start < len(token_ids):
                end = min(start + MAX_TOKENS, len(token_ids))
                chunk_ids = token_ids[start:end]
                text = tokenizer.decode(chunk_ids)

                roles = roles_for_department(department)

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "chunk_id": f"{file.name}::chunk_{idx}",
                            "source_path": str(file.name), # Store just filename for cleaner citations
                            "department": department,
                            "accessible_roles": ",".join(roles),
                        },
                    )
                )

                total_chunks += 1
                chunks_per_department[department] += 1

                idx += 1
                # Move window forward, but step back by OVERLAP to catch split context
                start += (MAX_TOKENS - OVERLAP)

    return {
        "documents": documents,
        "total_documents": len(documents),
        "total_chunks": total_chunks,
        "chunks_per_department": chunks_per_department,
    }