from typing import List


class PromptBuilder:
    def build_prompt(self, query: str, retrieved_chunks: List[str]) -> str:
        context = "\n\n---\n\n".join(retrieved_chunks)

        return f"""
Extract the answer from the context.

Question:
{query}

Context:
{context}

Instructions:
- Return only the options mentioned in the context.
- Use bullet points.
- Do not add explanation.
""".strip()