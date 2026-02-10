from backend.rag.retriever import secure_search_with_scores
from backend.rag.citation_utils import extract_citations
from backend.rag.confidence_utils import calculate_confidence_from_scores
from backend.llm.llm_client import LLMClient
from backend.llm.prompt_templates import build_prompt
from backend.rag.vector_store import get_vector_store

FALLBACK_MESSAGE = "The requested information is not available in the provided documents."


class RAGPipeline:
    def __init__(self):
        self.llm = LLMClient()

    # INCREASED k TO 15 TO FEED MORE DATA TO THE LLM
    def run(self, user_role: str, query: str, k: int = 15):
        vector_store = get_vector_store()  # ✅ lazy access

        results = secure_search_with_scores(
            vector_store,
            query,
            user_role,
            k,
        )

        if not results:
            return {
                "answer": FALLBACK_MESSAGE,
                "confidence": 0.0,
                "citations": [],
            }

        documents = [doc for doc, _ in results]
        prompt = build_prompt(query, documents)

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "confidence": calculate_confidence_from_scores(results),
            "citations": extract_citations(documents),
        }


rag_pipeline = RAGPipeline()