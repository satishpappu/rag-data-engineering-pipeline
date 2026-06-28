# RAG Data Engineering Pipeline

A modular Retrieval-Augmented Generation (RAG) pipeline demonstrating production-oriented document ingestion, semantic retrieval, and lightweight local response generation using Python, LangChain, SentenceTransformers, ChromaDB, and Hugging Face Transformers.

The project was built to understand the complete retrieval workflow from first principles, including document ingestion, normalization, chunking, embedding generation, vector indexing, semantic retrieval, prompt construction, and response generation.

---

# Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

# Architecture

```text
               Raw Documents
        (PDF / CSV / Markdown)
                     │
                     ▼
          Document Ingestion
                     │
                     ▼
      Canonical Document Schema
           (Pydantic Models)
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
      Semantic Similarity Retrieval
                     │
                     ▼
         Prompt Construction
                     │
                     ▼
      Hugging Face Local LLM
                     │
                     ▼
         Generated Response
```

---

# Features

* Modular document ingestion framework
* Canonical document normalization using Pydantic
* PDF, CSV, and Markdown ingestion
* Metadata extraction and lineage tracking
* Recursive semantic chunking using LangChain
* SentenceTransformer embedding generation
* Persistent vector indexing using ChromaDB
* Semantic similarity search using cosine similarity
* Prompt construction for grounded responses
* Lightweight local LLM-based response generation
* Config-driven architecture
* Centralized logging

---

# Tech Stack

| Component           | Technology                |
| ------------------- | ------------------------- |
| Language            | Python                    |
| Document Processing | LangChain                 |
| Embeddings          | SentenceTransformers      |
| Vector Database     | ChromaDB                  |
| Generation          | Hugging Face Transformers |
| Data Validation     | Pydantic                  |
| PDF Parsing         | PyPDF                     |
| Configuration       | YAML                      |
| Logging             | Python Logging            |

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
│   ├── query_vector_store.py
│   └── run_rag_query.py
│
├── src/
│
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── vectorstore/
│   ├── retrieval/
│   ├── generation/
│   │   ├── prompt_builder.py
│   │   └── llm_generator.py
│   │
│   ├── rag/
│   │   └── rag_pipeline.py
│   │
│   ├── orchestration/
│   └── utils/
│
└── README.md
```

---

# Canonical Document Schema

Every ingested document is normalized into a common schema before indexing.

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

| Type     | Supported |
| -------- | --------- |
| PDF      | Yes       |
| CSV      | Yes       |
| Markdown | Yes       |

---

# Chunking Strategy

This project uses LangChain's `RecursiveCharacterTextSplitter`.

Current configuration:

```yaml
chunk_size: 500
chunk_overlap: 100
```

Benefits:

* Preserves semantic context
* Maintains paragraph boundaries where possible
* Supports chunk overlap for retrieval continuity
* Improves semantic retrieval quality

---

# Embedding Model

Current embedding model:

```text
all-MiniLM-L6-v2
```

Reason for selection:

* Lightweight
* CPU-friendly
* Fast local inference
* Strong semantic similarity performance
* Well suited for local RAG development

---

# Vector Database

ChromaDB is used as the persistent vector store.

Features:

* Persistent local storage
* Cosine similarity search
* Lightweight deployment
* Fast semantic retrieval
* Simple developer experience

---

# Generation Layer

The retrieval pipeline has been extended with a lightweight generation layer to demonstrate a complete Retrieval-Augmented Generation workflow.

Pipeline:

```text
User Query
      │
      ▼
Semantic Retrieval
      │
      ▼
Prompt Construction
      │
      ▼
Local Hugging Face LLM
      │
      ▼
Generated Response
```

Current implementation uses:

```text
google/flan-t5-base
```

The generation component is isolated behind an `LLMGenerator` interface, allowing future replacement with:

* OpenAI GPT
* Claude
* Llama
* Mistral
* Ollama-hosted models

without changing the retrieval pipeline.

---

# Running the Project

## Index Documents

Place source documents inside:

```text
data/raw/
```

Run indexing:

```bash
PYTHONPATH=. python scripts/run_indexing.py
```

---

## Semantic Retrieval

```bash
PYTHONPATH=. python scripts/query_vector_store.py
```

Example query:

```python
query = "How does Delta Lake support ACID transactions?"
```

---

## End-to-End RAG Pipeline

```bash
PYTHONPATH=. python -m scripts.run_rag_query "What options does Databricks provide for ingesting data into Delta Lake?"
```

---

# Example Retrieval Output

```text
Result 1

Chunk ID:
databricks_deltalakeoverview_page_2_chunk_0

Content:

Atomic transactions with Delta Lake provide many options for updating data and metadata.
```

---

# Data Engineering Concepts Demonstrated

* Modular ingestion architecture
* Canonical document normalization
* Metadata lineage
* Recursive semantic chunking
* Embedding generation
* Vector persistence
* Semantic similarity retrieval
* Prompt construction
* Config-driven orchestration
* Production-oriented software design

---

# Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Metadata Filtering
* Cross-Encoder Re-ranking
* Similarity Thresholds
* Retrieval Evaluation Framework
* Guardrails
* Citation Verification
* Incremental Indexing
* Streaming Ingestion
* Pinecone / OpenSearch Integration
* Databricks Vector Search
* Airflow Orchestration
* Conversation Memory
* Agentic Workflows

---

# Learning Objectives

This project was built to deepen practical understanding of:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Embedding Models
* Production-style Data Engineering
* Prompt Construction
* Modular AI System Design

---

# Author

**Venkata Satish Pappu**

Senior Data Engineer | Python | PySpark | Databricks | AWS | Lakehouse Architecture | Generative AI | RAG Systems
