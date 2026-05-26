# RAG Data Engineering Pipeline

Production-style Retrieval-Augmented Generation (RAG) ingestion and semantic retrieval pipeline built using Python, LangChain, SentenceTransformers, and ChromaDB.

This project focuses on the data engineering side of RAG systems, including document ingestion, normalization, chunking, embedding generation, vector persistence, and semantic retrieval.

---

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

# Architecture

```text
Raw Documents (PDF / CSV / Markdown)
                │
                ▼
        Ingestion Loaders
                │
                ▼
     Canonical Document Schema
                │
                ▼
      Recursive Text Chunking
                │
                ▼
 SentenceTransformer Embeddings
                │
                ▼
       ChromaDB Vector Store
                │
                ▼
       Semantic Similarity Search
```

---

# Features

- Modular ingestion framework
- Canonical normalized document schema
- PDF, CSV, and Markdown ingestion
- Metadata extraction and lineage tracking
- LangChain recursive chunking
- SentenceTransformer local embeddings
- ChromaDB persistent vector storage
- Semantic retrieval using cosine similarity
- Config-driven architecture
- Centralized logging

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Chunking | LangChain |
| Embeddings | SentenceTransformers |
| Vector Database | ChromaDB |
| PDF Parsing | PyPDF |
| Data Validation | Pydantic |
| Configuration | YAML |
| Logging | Python Logging |

---

# Project Structure

```text
rag-data-engineering-pipeline/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── raw/
│
├── scripts/
│   ├── run_indexing.py
│   └── query_vector_store.py
│
├── src/
│   │
│   ├── ingestion/
│   │   ├── base_loader.py
│   │   ├── csv_loader.py
│   │   ├── markdown_loader.py
│   │   ├── pdf_loader.py
│   │   ├── document_normalizer.py
│   │   ├── ingestion_pipeline.py
│   │   └── models.py
│   │
│   ├── chunking/
│   │   └── document_chunker.py
│   │
│   ├── embeddings/
│   │   └── embedding_model.py
│   │
│   ├── vectorstore/
│   │   └── chroma_vector_store.py
│   │
│   ├── retrieval/
│   │   └── semantic_retriever.py
│   │
│   ├── orchestration/
│   │   └── indexing_orchestrator.py
│   │
│   └── utils/
│       ├── logger.py
│       └── config_loader.py
│
└── README.md
```

---

# Canonical Document Schema

All ingested documents are normalized into a unified schema.

```python
class Document(BaseModel):
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
    processing_status: ProcessingStatus
    chunk_count: int
```

---

# Supported Document Types

| Type | Supported |
|---|---|
| PDF | Yes |
| CSV | Yes |
| Markdown | Yes |

---

# Chunking Strategy

This project uses LangChain's `RecursiveCharacterTextSplitter`.

Benefits:

- Preserves semantic context
- Maintains paragraph structure where possible
- Supports chunk overlap for retrieval continuity
- Improves semantic search quality

Current configuration:

```yaml
chunking:
  chunk_size: 500
  chunk_overlap: 100
```

---

# Embedding Model

Embedding model:

```text
all-MiniLM-L6-v2
```

Why this model?

- Lightweight
- CPU friendly
- Fast local inference
- Strong semantic similarity performance
- Ideal for local RAG MVPs

---

# Vector Database

This project uses ChromaDB as the vector store.

Features:

- Persistent local vector storage
- Cosine similarity search
- Lightweight local deployment
- Fast semantic retrieval

---

# Running the Project

## 1. Create Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

## 2. Install Dependencies

```bash
pip install torch
pip install "numpy<2"

pip install \
sentence-transformers==2.6.1 \
"transformers<4.40" \
langchain-text-splitters \
chromadb \
pypdf \
pandas \
pyyaml
```

---

# Index Documents

Place documents inside:

```text
data/raw/
```

Run indexing:

```bash
PYTHONPATH=. python scripts/run_indexing.py
```

---

# Query the Vector Store

Run semantic retrieval:

```bash
PYTHONPATH=. python scripts/query_vector_store.py
```

Example query:

```python
query = "How does Delta Lake support ACID transactions?"
```

---

# Example Retrieval Output

```text
Result 1
Chunk ID: databricks_deltalakeoverview_page_2_chunk_0

Content:

Atomic transactions with Delta Lake provide many options for updating data and metadata.
```

---

# Key Data Engineering Concepts Demonstrated

- Canonical normalization
- Metadata lineage
- Modular ingestion architecture
- Semantic chunking
- Embedding generation
- Vector persistence
- Semantic similarity retrieval
- Config-driven orchestration
- Production-style pipeline design

---

# Future Improvements

- Hybrid retrieval (BM25 + vector search)
- Metadata filtering
- Reranking models
- LLM response generation
- Incremental indexing
- Deduplication framework
- Streaming ingestion support
- OpenSearch / Pinecone integration
- Airflow orchestration
- Databricks integration
- Evaluation framework

---

# Learning Goals

This project was designed to explore:

- RAG architecture fundamentals
- Semantic search systems
- Vector databases
- Production-oriented ingestion design
- Data engineering patterns for GenAI systems

---

# Author

Venkata Satish Pappu

Senior Data Engineer | Python | PySpark | Databricks | AWS | Lakehouse Architecture | RAG Systems