from typing import List, Dict, Any

from src.generation.prompt_builder import PromptBuilder
from src.generation.llm_generator import LLMGenerator


class RAGPipeline:
    def __init__(self, retriever):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm_generator = LLMGenerator()

    def answer(self, query: str, top_k: int = 3) -> str:
        results: List[Dict[str, Any]] = self.retriever.retrieve(
            query=query,
            top_k=top_k
        )

        print("\nRetrieved Context:\n")
        for idx, result in enumerate(results, start=1):
            print("=" * 80)
            print(f"Chunk {idx}")
            print(f"Chunk ID: {result.get('chunk_id')}")
            print(f"Distance: {result.get('distance')}")
            print(result["content"][:800])

        retrieved_chunks = [
            result["content"]
            for result in results
            if result.get("distance", 999) < 0.45
        ]

        if not retrieved_chunks:
            return "I don't have enough information from the retrieved documents."

        prompt = self.prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks
        )

        return self.llm_generator.generate(prompt)