from src.embeddings.EmbeddingModel import EmbeddingModel
from src.vectorstore.ChromaVectorStore import ChromaVectorStore


class SemanticRetriever:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = ChromaVectorStore()

    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_model.embed_query(query)
        results = self.vector_store.query(query_embedding, top_k)

        retrieved_chunks = []

        for i in range(len(results["ids"][0])):
            retrieved_chunks.append({
                "chunk_id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return retrieved_chunks