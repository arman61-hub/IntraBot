from typing import List, Tuple
from langchain_core.documents import Document
from langchain_chroma import Chroma

def role_allowed(doc: Document, user_role: str) -> bool:
    roles = {
        r.strip()
        for r in doc.metadata.get("accessible_roles", "").split(",")
    }
    return user_role in roles


def secure_search_with_scores(
    vector_store: Chroma,
    query: str,
    role: str,
    k: int = 5,
) -> List[Tuple[Document, float]]:

    results = vector_store.similarity_search_with_score(query, k=k * 5)

    safe_results: List[Tuple[Document, float]] = []

    for doc, score in results:
        if not role_allowed(doc, role):
            continue

        safe_results.append((doc, score))

        if len(safe_results) == k:
            break

    return safe_results
