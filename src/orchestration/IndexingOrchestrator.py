from src.ingestion.ingestion_pipeline import IngestionPipeline
from src.chunking.DocumentChunker import DocumentChunker
from src.embeddings.EmbeddingModel import EmbeddingModel
from src.vectorstore.ChromaVectorStore import ChromaVectorStore

from src.utils.logger import get_logger
from src.utils.config_loader import load_config


class IndexingOrchestrator:

    def __init__(self, config_path: str):

        self.logger = get_logger(self.__class__.__name__)

        self.config = load_config(config_path)

        self.ingestion_pipeline = IngestionPipeline()

        self.chunker = DocumentChunker(
            chunk_size=self.config["chunking"]["chunk_size"],
            chunk_overlap=self.config["chunking"]["chunk_overlap"]
        )

        self.embedding_model = EmbeddingModel(
            model_name=self.config["embedding"]["model_name"]
        )

        self.vector_store = ChromaVectorStore(
            persist_path=self.config["vectorstore"]["persist_path"],
            collection_name=self.config["vectorstore"]["collection_name"]
        )

    def run(self, input_path: str):

        self.logger.info("Starting indexing pipeline")

        documents = self.ingestion_pipeline.run(input_path)

        self.logger.info(f"Documents loaded: {len(documents)}")

        all_chunks = []

        for document in documents:

            chunks = self.chunker.chunk_document(document)

            self.logger.info(
                f"Generated {len(chunks)} chunks "
                f"for document {document.file_name}"
            )

            all_chunks.extend(chunks)

        self.logger.info(f"Total chunks generated: {len(all_chunks)}")

        chunk_texts = [chunk["content"] for chunk in all_chunks]

        self.logger.info("Generating embeddings")

        embeddings = self.embedding_model.embed_texts(chunk_texts)

        self.logger.info("Persisting embeddings to ChromaDB")

        self.vector_store.add_chunks(all_chunks, embeddings)

        self.logger.info(
            f"Vector store document count: "
            f"{self.vector_store.count()}"
        )

        self.logger.info("Indexing pipeline completed successfully")