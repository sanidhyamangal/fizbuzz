import typing as t

from llama_index.core.agent import ReActAgent

from fizbuzz.tools.yahoo_finance import YahooFinanceToolSpec

from ..llms.openai import OpenAILLM


class FinanceAgent:
    def __init__(self, llm: OpenAILLM, verbose: bool = False) -> None:
        self.llm = llm.get_default_llm()
        finance_tools = YahooFinanceToolSpec().to_tool_list()
        self.agent = ReActAgent.from_tools(
            finance_tools, llm=self.llm, max_iterations=10, verbose=verbose
        )

    def chat(self, query: str) -> t.Any:
        response = self.agent.chat(query)
        return response
