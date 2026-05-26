from src.ingestion.base_loader import BaseLoader


class MarkdownLoader(BaseLoader):

    def load(self) -> str:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    def extract_metadata(self):
        return {
            "source_type": "markdown"
        }

    def normalize(self):
        return self.load()