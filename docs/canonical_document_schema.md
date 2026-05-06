# Overview
This project spans across multiple sources/categories like public technical documentation, enterprise runbooks, operational metadata, data quality rules and incident records.

Multiple source formats are standardized into a unified document schema to simplify downstream processing including validation, chunking, embedding generation, metadata enrichment, and retrieval.

A canonical document schema enables downstream components such as validation, chunking, embedding generation, retrieval, and metadata filtering to operate independently of the original source format. This reduces parser-specific complexity and improves scalability and maintainability of the ingestion pipeline.

The ingestion layer acts as the normalization boundary between heterogeneous upstream sources and downstream retrieval systems.
## Supported source formats
- PDF: External technical documentation
- Markdown: Internal enterprise runbooks
- CSV: Operational metadata and governance datasets

## Canonical Schema
### Core fields
| Field               | Description                         |
| ------------------- | ----------------------------------- |
| document_id         | unique document identifier          |
| source_type         | pdf/csv/markdown                    |
| document_category   | technical_documentation,enterprise_runbook,operational_metadata,data_quality_rule,incident_record |
| file_name           | original source file                |
| content             | normalized text                     |

### Operational Metadata fields
| Field               | Description                         |
| ------------------- | ----------------------------------- |
| ingestion_timestamp | ingestion time                      |
| source_system     | provenance         |
| ingestion_job_id  | lineage/debugging  |
| content_hash      | deduplication      |
| processing_status | pipeline tracking  |
| chunk_count       | downstream metrics |

## Sample JSON
### PDF
{
  "document_id": "doc_001",
  "source_type": "pdf",
  "document_category": "technical_documentation",
  "file_name": "snowflake_timetravel.pdf",
  "content": "Time Travel enables historical data access...",
  "metadata": {
    "source_system": "snowflake_docs",
    "ingestion_timestamp": "2026-05-06T12:00:00",
    "page_number": 3,
    "author": "Snowflake",
    "tags": ["time_travel", "recovery"]
  }
}

## Why metadata matters

Metadata enables traceability of ingested content across the pipeline lifecycle. It supports source attribution, chunk lineage tracking, retrieval filtering, auditability, and operational observability. Metadata also improves retrieval precision by enabling category-based and source-aware filtering during semantic search.

## Canonicalization philosophy
The core principle of canonicalization is to maintain a normalized schema irrespective of the parser type. This idea stems from the fact that the downstream systems should operate independently of the original source format.

## Future enhancements
- versioning
- schema evolution
- incremental ingestion
- document deduplication
- chunk-level lineage tracking
- vector index versioning