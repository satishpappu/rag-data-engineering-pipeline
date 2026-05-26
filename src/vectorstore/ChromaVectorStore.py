import chromadb


class ChromaVectorStore:
    def __init__(
        self,
        persist_path: str = "vector_db/chroma",
        collection_name: str = "rag_documents"
    ):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        self.collection.add(
            ids=[chunk["chunk_id"] for chunk in chunks],
            documents=[chunk["content"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
            embeddings=embeddings
        )

    def query(self, query_embedding: list[float], top_k: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

    def count(self) -> int:
        return self.collection.count()