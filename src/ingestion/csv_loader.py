import pandas as pd

from src.ingestion.base_loader import BaseLoader


class CSVLoader(BaseLoader):

    def load(self) -> str:
        df = pd.read_csv(self.file_path)
        return df.to_string(index=False)

    def extract_metadata(self):
        return {
            "source_type": "csv"
        }

    def normalize(self):
        return self.load()