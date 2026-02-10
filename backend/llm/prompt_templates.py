from typing import List
from langchain_core.documents import Document

def build_prompt(query: str, documents: List[Document]) -> str:
    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source_path', 'Unknown')}]\n{doc.page_content.strip()}"
        for doc in documents
    )

    SYSTEM_PROMPT = (
        "You are an internal company assistant.\n"
        "Use the provided context to answer the user's question.\n"
        "If partial information is available, summarize what is present.\n"
        "Be concise. Provide a summary if the answer is long.\n"
        "Do NOT refuse to answer if the information is incomplete.\n"
        "Do NOT add external knowledge.\n"
        "Answer in clear bullet points.\n"
    )

    return f"""
            {SYSTEM_PROMPT}

            ### Context Data:
            {context}

            ### User Question:
            {query}

            ### Answer:
            """