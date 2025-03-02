import os
import typing as t

from llama_index.llms.openai import OpenAI


class OpenAILLM:
    @classmethod
    def get_llm(cls, **llm_args: dict[str, t.Any]) -> OpenAI:
        return OpenAI(**llm_args)

    @classmethod
    def get_default_llm(
        cls,
        model: str = os.getenv("OPENAI_MODEL", "o3-mini"),
        temprature: float = 0.0,
        max_retries: int = 5,
        timeout: float = 120.0,
        reasoning_effort: str = "high",
        **llm_args: dict[str, t.Any],
    ) -> OpenAI:
        return cls.get_llm(
            model=model,
            temprature=temprature,
            max_retries=max_retries,
            timeout=timeout,
            reasoning_effort=reasoning_effort,
            **llm_args,
        )
