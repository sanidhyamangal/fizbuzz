"""
author: Sanidhya Mangal
email: mangalsanidhya19@gmail.com
"""

from argparse import ArgumentParser
from dataclasses import dataclass

import pandas as pd
import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="yahoo_finance_mcp",
    instructions="""
    You are a Yahoo Finance MCP agent. 
    You can answer questions about stocks, including their price, news and analyst recommendations.
    """,
)


@mcp.tool()
def balance_sheet(ticker: str) -> str:
    """A function to download balance sheet from yahoo finance for a given ticker

    Args:
        ticker (str): A stock ticker to be given to yahoo finance

    Returns:
        str: balance sheet of given stock ticker
    """

    stock = yf.Ticker(ticker=ticker)
    balance_sheet = pd.DataFrame(stock.balance_sheet)
    return f"Balance Sheet:\n{balance_sheet.to_string()}"


@mcp.tool()
def cash_flow(ticker: str) -> str:
    """A function to return chashflow of a stock from yahoo finance

    Args:
        ticker (str): A stock ticker to be given to yahoo finance

    Returns:
        str: cash flow of a given stock ticker
    """

    stock = yf.Ticker(ticker=ticker)
    cash_flow = pd.DataFrame(stock.cash_flow)
    return f"Cash Flow:\n{cash_flow.to_string()}"


@mcp.tool()
def basic_stock_information(ticker: str) -> str:
    """A function to return basic stock information. Eg. price, description, name

    Args:
        ticker (str): A stock ticker to be given to yahoo finance

    Returns:
        str: basic stock information of a given stock
    """

    stock = yf.Ticker(ticker=ticker)
    return f"Basic Stock information:\n{stock.info}"


@mcp.tool()
def analyst_recommendations(ticker: str) -> str:
    """Get the analyst recommendations for the stocks

    Args:
        ticker (str): the stock ticker to be given to yfinance

    Returns:
        str: analyst recommendations for the given stock ticker
    """
    stock = yf.Ticker(ticker)
    return f"Recommendations:\n{stock.recommendations}"


@mcp.tool()
def stock_news(ticker: str) -> str:
    """Get most recent news titles for the stock

    Args:
        ticker (str): the stock ticker to be given to yfinance

    Returns:
        str: most recent news for the given stock ticker
    """
    stock = yf.Ticker(ticker=ticker)
    stock_news = stock.news
    titles = "\n".join(news["content"]["title"] for news in stock_news)
    return f"News:\n{titles}"


@mcp.tool()
def income_statement(ticker: str) -> str:
    """Get income statement for the stock

    Args:
        ticker (str): the stock ticker to be given to yfinance

    Returns:
        str: income statement for the given stock ticker
    """

    stock = yf.Ticker(ticker)
    income_statement = pd.DataFrame(stock.income_stmt)
    return f"Income Statement:\n{income_statement.to_string()}"


def main():
    @dataclass
    class CommandLineArgs:
        server_type: str

    argparser = ArgumentParser("Yahoo Finance MCP server")
    argparser.add_argument(
        "--server_type",
        type=str,
        default="sse",
        help="Server type to use",
        choices=("sse", "streamable-http", "stdio"),
    )

    args = CommandLineArgs(**vars(argparser.parse_args()))

    mcp.run(
        transport=args.server_type,
    )
