import sys

from src.retrieval.SemanticRetriever import SemanticRetriever
from src.rag.rag_pipeline import RAGPipeline


def main():
    if len(sys.argv) < 2:
        raise ValueError(
            "Usage: python scripts/run_rag_query.py 'your question'"
        )

    query = sys.argv[1]

    retriever = SemanticRetriever()
    rag_pipeline = RAGPipeline(retriever=retriever)

    answer = rag_pipeline.answer(query=query, top_k=3)

    print("\nGenerated Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()