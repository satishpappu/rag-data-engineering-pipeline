from src.retrieval.SemanticRetriever import SemanticRetriever


def main():

    retriever = SemanticRetriever()

    query = "How does Delta Lake support ACID transactions?"

    results = retriever.retrieve(query=query, top_k=3)

    for idx, result in enumerate(results, start=1):

        print("\n" + "=" * 80)
        print(f"Result {idx}")

        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Distance: {result['distance']}")

        metadata = result["metadata"]

        print(f"File: {metadata.get('file_name')}")

        print("\nContent:\n")
        print(result["content"][:1200])


if __name__ == "__main__":
    main()