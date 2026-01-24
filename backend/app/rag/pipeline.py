from backend.app.rag.rbac import get_allowed_dirs
from backend.app.rag.preprocessing import preprocess
from backend.app.rag.vector_store import build_vector_store


def run_pipeline(role: str):
    directories = get_allowed_dirs(role)
    result = preprocess(directories)
    store = build_vector_store(result["documents"])

    return {
        "vector_store": store,
        "total_documents": result["total_documents"],
        "total_chunks": result["total_chunks"],
    }
