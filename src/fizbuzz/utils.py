import logging
import os
import typing as t

from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from rich.console import Console
from rich.logging import RichHandler

# from llama_index.core.agent.workflow import FunctionAgent, ToolCall, ToolCallResult
# from llama_index.core.llms.function_calling import FunctionCallingLLM


def configure_logging(
    level: t.Literal["DEBUG", "INFO", "WARN", "CRITICAL", "ERROR"] = "INFO",
):
    handlers: list[logging.Handler] = []

    handlers.append(
        RichHandler(level=level, console=Console(stderr=True), rich_tracebacks=True)
    )

    if not handlers:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(level=level, format="%(message)s", handlers=handlers)


def get_default_ollama_llm(temperature: float, **options: dict) -> Ollama:
    """Get Ollama instance to query for data

    Args:
        temperature (float): temperature param for llm

    Returns:
        Ollama: A function calling LLM to run agentic functions
    """

    return Ollama(
        model=os.getenv("OLLAMA_MODEL"), temperature=temperature, request_timeout=120.0
    )


async def get_mcp_tools(url: str) -> McpToolSpec:
    """Get list of mcp tools using sse url

    Args:
        url (str): url to stream mcp tools

    Returns:
        McpToolSpec: ToolSpec for MCP agent
    """

    mcp_client = BasicMCPClient(f"{url}/sse")
    mcp_tool_spec = McpToolSpec(client=mcp_client)

    tools = await mcp_tool_spec.to_tool_list_async()

    return tools
