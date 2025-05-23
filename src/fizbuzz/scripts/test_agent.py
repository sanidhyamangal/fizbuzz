import asyncio
import os

from dotenv import load_dotenv

from fizbuzz.agents.finance_agent import FinanceAgent
from fizbuzz.utils import configure_logging, get_default_ollama_llm

load_dotenv(override=True)

configure_logging()


async def main():
    llm = get_default_ollama_llm(temperature=0.3)
    fa = await FinanceAgent.create(
        mcp_url=os.getenv("FINANCE_MCP_URL"), verbose=True, llm=llm
    )

    response = await fa.handle_user_request("What do analyst say about Nvidia?")

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
