from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from src.ingestion.models import Document

class BaseLoader(ABC):
    """
    Abstract base class for all document loaders.

    Each source-specific loader must know how to:
    1. load raw content
    2. extract source-specific metadata
    3. normalize content into canonical Document objects
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    @abstractmethod
    def load(self) -> Any:
        """Load raw content from the source file."""
        pass

    @abstractmethod
    def extract_metadata(self) -> Dict[str, Any]:
        """Extract source-specific metadata."""
        pass

    @abstractmethod
    def normalize(self) -> List[Document]:
        """Convert loaded content into canonical Document objects."""
        pass