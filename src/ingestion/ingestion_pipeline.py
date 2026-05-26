import os
from typing import List

from src.ingestion.csv_loader import CSVLoader
from src.ingestion.markdown_loader import MarkdownLoader
from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.document_normalizer import DocumentNormalizer
from src.ingestion.models import Document, SourceType


class IngestionPipeline:
    def __init__(self):
        self.normalizer = DocumentNormalizer()

        self.loader_mapping = {
            ".csv": CSVLoader,
            ".md": MarkdownLoader,
        }

        self.source_type_mapping = {
            ".csv": SourceType.CSV,
            ".md": SourceType.MARKDOWN,
        }

    def run(self, input_path: str) -> List[Document]:
        documents: List[Document] = []

        for root, _, files in os.walk(input_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                extension = os.path.splitext(file_name)[1].lower()

                if extension == ".pdf":
                    loader = PDFLoader(file_path)
                    pdf_documents = loader.normalize()
                    documents.extend(pdf_documents)
                    continue

                if extension not in self.loader_mapping:
                    continue

                loader_class = self.loader_mapping[extension]
                loader = loader_class(file_path)

                raw_content = loader.load()

                document = self.normalizer.normalize(
                    file_path=file_path,
                    content=raw_content,
                    source_type=self.source_type_mapping[extension],
                )

                documents.append(document)

        return documents