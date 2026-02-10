from backend.rag.preprocessing import preprocess
from backend.rag.vector_store import build_vector_store
from pathlib import Path

BASE_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "Fintech-data"

EXPECTED_FOLDERS = {
    "finance",
    "marketing",
    "hr",
    "engineering",
    "general",
}


def run_pipeline_once():
    directories = [d for d in BASE_DATA_PATH.iterdir() if d.is_dir()]
    folder_names = {d.name.lower() for d in directories}

    missing = EXPECTED_FOLDERS - folder_names
    if missing:
        raise RuntimeError(
            f"❌ Missing required data folders: {sorted(missing)}"
        )

    result = preprocess(directories)
    build_vector_store(result["documents"])

    return {
        "total_documents": result["total_documents"],
        "total_chunks": result["total_chunks"],
        "chunks_per_department": result["chunks_per_department"],
    }
