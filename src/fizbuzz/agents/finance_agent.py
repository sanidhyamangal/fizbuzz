from logging import getLogger

from llama_index.core.agent.workflow import FunctionAgent, ToolCall, ToolCallResult
from llama_index.core.llms.function_calling import FunctionCallingLLM

from ..utils import get_mcp_tools

logger = getLogger(__name__)

SYSTEM_PROMPT = """
Act as a Finance Agent, capable of interacting with YahooFinance API via tool calling.

Before you can interact with the User, you need to work with tools that calls Yahoo Finance API.
"""


class FinanceAgent:
    def __init__(self, agent: FunctionAgent, verbose: bool = False) -> None:
        self.verbose = verbose
        self.agent = agent

    @classmethod
    async def create(
        cls, mcp_url: str, llm: FunctionCallingLLM, verbose: bool = False
    ) -> "FinanceAgent":
        tools = await get_mcp_tools(mcp_url)
        agent = FunctionAgent(
            name="FinAgent",
            description="An AI agent to interact with yahoo finance mcp server and respond to user query",
            llm=llm,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )
        return cls(agent=agent, verbose=verbose)

    async def handle_user_request(self, query: str) -> str:
        handler = self.agent.run(user_msg=query.lower())

        async for event in handler.stream_events():
            if self.verbose and isinstance(event, ToolCall):
                logger.info(
                    f"Tool Call: {event.tool_name} with args: {event.tool_kwargs}"
                )
            elif self.verbose and isinstance(event, ToolCallResult):
                logger.info(
                    f"Tool Call: {event.tool_name} with output: {event.tool_output}"
                )

        response = await handler
        return str(response)
