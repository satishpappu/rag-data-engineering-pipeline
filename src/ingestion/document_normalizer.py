import hashlib
import os
from datetime import datetime, timezone

from src.ingestion.models import Document, SourceType, DocumentCategory, ProcessingStatus


class DocumentNormalizer:

    def normalize(
        self,
        file_path: str,
        content: str,
        source_type: SourceType,
        document_category: DocumentCategory = DocumentCategory.TECHNICAL_DOCUMENTATION,
        source_system: str = "local_file_system"
    ) -> Document:

        file_name = os.path.basename(file_path)
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        document_id = hashlib.md5(
            f"{file_name}_{content_hash}".encode("utf-8")
        ).hexdigest()

        return Document(
            document_id=document_id,
            source_type=source_type,
            document_category=document_category,
            file_name=file_name,
            content=content,
            metadata={
                "file_path": file_path,
                "file_extension": os.path.splitext(file_name)[1],
            },
            ingestion_timestamp=datetime.now(timezone.utc),
            source_system=source_system,
            ingestion_job_id=f"job_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            content_hash=content_hash,
            processing_status=ProcessingStatus.INGESTED,
            chunk_count=0
        )