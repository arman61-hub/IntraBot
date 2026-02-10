from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
import shutil

PERSIST_DIR = "backend/vector_db/chroma"
_COLLECTION_NAME = "company_docs"

_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_vector_store: Chroma | None = None


# Build vector store from scratch (used at app startup).
def build_vector_store(documents: List[Document]) -> Chroma:
    
    global _vector_store
    
    persist_path = Path(PERSIST_DIR)
    if persist_path.exists():
        shutil.rmtree(persist_path)

    print("🔄 Building vector store...")
    print(f"📄 Incoming documents: {len(documents)}")

    _vector_store = Chroma.from_documents(
        documents=documents,
        embedding=_embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=_COLLECTION_NAME,
    )

    print("🔍 VECTOR STORE CHECK")
    print("Total documents in DB:", _vector_store._collection.count())

    return _vector_store


# Lazy-load vector store for query-time access.
def get_vector_store() -> Chroma:

    global _vector_store

    if _vector_store is not None:
        return _vector_store

    persist_path = Path(PERSIST_DIR)
    if not persist_path.exists():
        raise RuntimeError(
            "❌ Vector store not found. Startup ingestion may have failed."
        )

    print("📦 Loading existing vector store from disk...")

    _vector_store = Chroma(
        embedding_function=_embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=_COLLECTION_NAME,
    )

    print("🔍 VECTOR STORE CHECK")
    print("Total documents in DB:", _vector_store._collection.count())

    return _vector_store
