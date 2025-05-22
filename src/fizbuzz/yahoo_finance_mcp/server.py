"""
author: Sanidhya Mangal
email: mangalsanidhya19@gmail.com
"""

from logging import getLogger

import click
import uvicorn
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport

# from mcp.server.fastmcp.utilities.logging import configure_logging, get_logger
from mcp.types import TextContent, Tool
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Mount, Route

from .functions import StockInput, StockToolList, StockTools
from .utils import configure_logging

logger = getLogger(__name__)
configure_logging(level="INFO")


@click.command()
@click.option(
    "--server_type",
    type=click.Choice(["sse", "stdio"]),
    default="sse",
    help="server type to use",
)
def main(server_type: str):
    server = Server(
        "yf-finance-mcp",
        version="1.0.0",
        instructions="A MCP server responsible to call all the Yahoo finance related APIs using defined functions",
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=StockToolList.CASH_FLOW,
                description="Retrieve cash flow information for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
            Tool(
                name=StockToolList.BALANCE_SHEET,
                description="Show balance sheet for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
            Tool(
                name=StockToolList.ANALYST_RECOMMENDATIONS,
                description="Retrieve analyst recommendations for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
            Tool(
                name=StockToolList.INCOME_STATEMENT,
                description="Describes income statment for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
            Tool(
                name=StockToolList.BASIC_STOCK_INFORMATION,
                description="Basic stock information such as rate, company history, etc for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
            Tool(
                name=StockToolList.STOCK_NEWS,
                description="Retrieve top 5 news title for a stock ticker",
                inputSchema=StockInput.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        logger.info(f"Tool Call: {name} with arguments: {arguments}")
        stock_ticker = arguments.pop("stock_ticker")

        if stock_ticker is None:
            raise ValueError("No stock ticker present for tool call")

        match name:
            case StockToolList.ANALYST_RECOMMENDATIONS:
                result = StockTools.stock_news(stock_ticker)
                return [
                    TextContent(
                        type="text",
                        text=result,
                    )
                ]
            case StockToolList.BASIC_STOCK_INFORMATION:
                result = StockTools.basic_stock_information(stock_ticker)
                return [TextContent(type="text", text=result)]
            case StockToolList.BALANCE_SHEET:
                result = StockTools.balance_sheet(stock_ticker)
                return [TextContent(type="text", text=result)]
            case StockToolList.CASH_FLOW:
                result = StockTools.cash_flow(stock_ticker)
                return [TextContent(type="text", text=result)]
            case StockToolList.INCOME_STATEMENT:
                result = StockTools.income_statement(stock_ticker)
                return [TextContent(type="text", text=result)]

            case StockToolList.STOCK_NEWS:
                result = StockTools.stock_news(stock_ticker)
                return [TextContent(type="text", text=result)]

            case _:
                raise ValueError(f"Unkown tool:{name}")

    if server_type == "sse":
        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await server.run(
                    streams[0], streams[1], server.create_initialization_options()
                )

            return Response()

        app = Starlette(
            debug=True,
            routes=[
                Route("/yf/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        uvicorn.run(
            app=app,
        )
