from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_document(self, document):
        chunks = self.splitter.split_text(document.content)

        return [
            {
                "chunk_id": f"{document.document_id}_chunk_{i}",
                "document_id": document.document_id,
                "content": chunk,
                "metadata": {
                    "document_id": document.document_id,
                    "file_name": document.file_name,
                    "source_type": document.source_type.value,
                    "document_category": document.document_category.value,
                    "chunk_index": i,
                    "source_system": document.source_system,
                }
            }
            for i, chunk in enumerate(chunks)
        ]