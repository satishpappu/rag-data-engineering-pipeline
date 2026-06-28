from transformers import pipeline


class LLMGenerator:
    def __init__(self, model_name: str = "google/flan-t5-base"):
        self.generator = pipeline(
            "text2text-generation",
            model=model_name
        )

    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        response = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

        return response[0]["generated_text"]