from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from enum import Enum

class SourceType(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    MARKDOWN = "markdown"

class DocumentCategory(str, Enum):
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    ENTERPRISE_RUNBOOK = "enterprise_runbook"
    OPERATIONAL_METADATA = "operational_metadata"
    DATA_QUALITY_RULE = "data_quality_rule"
    INCIDENT_RECORD = "incident_record"

class ProcessingStatus(str, Enum):
    INGESTED = "ingested"
    IN_PROGRESS = "in_progress"
    QUEUED = "queued"
    FAILED = "failed"

class Document(BaseModel):
    """
    Canonical normalized document schema used across the ingestion pipeline.
    """
    document_id: str
    source_type: SourceType
    document_category: DocumentCategory
    file_name: str
    content: str
    metadata: Dict[str, Any]
    ingestion_timestamp: datetime
    source_system: str
    ingestion_job_id: str
    content_hash: str
    processing_status: ProcessingStatus = ProcessingStatus.INGESTED
    chunk_count: int = 0
