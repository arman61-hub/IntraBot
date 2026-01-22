import hashlib
from typing import List
import re

from langchain_core.documents import Document
from langchain_chroma import Chroma
from backend.app.rag.rbac import get_effective_roles


def normalize_query(query: str) -> str:
    query = query.lower()
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def _role_allowed(accessible_roles: str, user_role: str) -> bool:
    doc_roles = {r.strip() for r in accessible_roles.split(",")}
    user_roles = get_effective_roles(user_role)
    return not doc_roles.isdisjoint(user_roles)


def _content_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def secure_search(
    vector_store: Chroma,
    query: str,
    role: str,
    k: int = 5,
) -> List[Document]:

    normalized_query = normalize_query(query)

    results = vector_store.similarity_search(
        normalized_query,
        k=k * 5,   # high recall
    )

    seen = set()
    safe_results: List[Document] = []

    for doc in results:
        if not _role_allowed(doc.metadata.get("accessible_roles", ""), role):
            continue

        dedup_key = (
            doc.metadata.get("source_path"),
            _content_hash(doc.page_content[:300])
        )

        if dedup_key in seen:
            continue

        seen.add(dedup_key)
        safe_results.append(doc)

        if len(safe_results) == k:
            break

    return safe_results
