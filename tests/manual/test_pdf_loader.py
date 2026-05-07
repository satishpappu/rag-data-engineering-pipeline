from src.ingestion.pdf_loader import PDFLoader

pdf_path = "data/raw/public_docs/snowflake_timetravel.pdf"

loader = PDFLoader(pdf_path)
documents = loader.normalize()

print(f"Total normalized documents: {len(documents)}")

first_doc = documents[0]

print("\n--- First Document ---")
print(f"Document ID: {first_doc.document_id}")
print(f"Source Type: {first_doc.source_type}")
print(f"Category: {first_doc.document_category}")
print(f"File Name: {first_doc.file_name}")
print(f"Source System: {first_doc.source_system}")
print(f"Page Number: {first_doc.metadata.get('page_number')}")
print(f"Content Hash: {first_doc.content_hash[:12]}")
print("\nContent Preview:")
print(first_doc.content[:500])