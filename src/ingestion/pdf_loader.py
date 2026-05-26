import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from pypdf import PdfReader

from src.ingestion.base_loader import BaseLoader
from src.ingestion.models import (
    Document,
    DocumentCategory,
    ProcessingStatus,
    SourceType,
)


class PDFLoader(BaseLoader):
    """
    Loader for PDF documents.
    Each PDF page is normalized as one canonical Document.
    """

    def load(self) -> PdfReader:
        return PdfReader(str(self.file_path))

    def extract_metadata(self) -> Dict[str, Any]:
        reader = self.load()
        pdf_metadata = reader.metadata or {}

        return {
            "title": pdf_metadata.get("/Title"),
            "author": pdf_metadata.get("/Author"),
            "producer": pdf_metadata.get("/Producer"),
            "total_pages": len(reader.pages),
        }

    def normalize(self) -> List[Document]:
        reader = self.load()
        base_metadata = self.extract_metadata()

        documents: List[Document] = []
        ingestion_job_id = str(uuid4())

        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()

            if not text:
                continue

            content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

            metadata = {
                **base_metadata,
                "page_number": page_index,
            }

            document = Document(
                document_id=f"{self.file_path.stem}_page_{page_index}",
                source_type=SourceType.PDF,
                document_category=DocumentCategory.TECHNICAL_DOCUMENTATION,
                file_name=self.file_path.name,
                content=text,
                metadata=metadata,
                ingestion_timestamp=datetime.now(timezone.utc),
                source_system="public_docs",
                ingestion_job_id=ingestion_job_id,
                content_hash=content_hash,
                processing_status=ProcessingStatus.INGESTED,
                chunk_count=0,
            )

            documents.append(document)

        return documents