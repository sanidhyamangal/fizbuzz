"""
author: Sanidhya Mangal
email: mangalsanidhya19@gmail.com
"""

import pandas as pd
import yfinance as yf
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class YahooFinanceToolSpec(BaseToolSpec):
    """A Tool to pull all the financial data from yahoo finance
    and serve it in a LLM readable format.
    """

    spec_functions = [
        "balance_sheet",
        "cash_flow",
        "income_statement",
        "basic_stock_information",
        "analyst_recommendations",
        "stock_news",
    ]

    def __init__(self):
        """Initialize the Yahoo Finance tool spec."""

    def balance_sheet(self, ticker: str) -> str:
        """A function to download balance sheet from yahoo finance for a given ticker

        Args:
            ticker (str): A stock ticker to be given to yahoo finance
        """

        stock = yf.Ticker(ticker=ticker)
        balance_sheet = pd.DataFrame(stock.balance_sheet)
        return f"Balance Sheet:\n{balance_sheet.to_string()}"

    def cash_flow(self, ticker: str) -> str:
        """A function to return chashflow of a stock from yahoo finance

        Args:
            ticker (str): A stock ticker to be given to yahoo finance
        """

        stock = yf.Ticker(ticker=ticker)
        cash_flow = pd.DataFrame(stock.cash_flow)
        return f"Cash Flow:\n{cash_flow.to_string()}"

    def basic_stock_information(self, ticker: str) -> str:
        """A function to return basic stock information. Eg. price, description, name

        Args:
            ticker (str): A stock ticker to be given to yahoo finance
        """

        stock = yf.Ticker(ticker=ticker)
        return f"Basic Stock information:\n{stock.info}"

    def analyst_recommendations(self, ticker: str) -> str:
        """Get the analyst recommendations for the stocks

        Args:
            ticker (str): the stock ticker to be given to yfinance
        """
        stock = yf.Ticker(ticker)
        return f"Recommendations:\n{stock.recommendations}"

    def stock_news(self, ticker: str) -> str:
        """Get most recent news titles for the stock

        Args:
            ticker (str): the stock ticker to be given to yfinance
        """
        stock = yf.Ticker(ticker=ticker)
        stock_news = stock.news
        titles = "\n".join(news["content"]["title"] for news in stock_news)
        return f"News:\n{titles}"

    def income_statement(self, ticker: str) -> str:
        """Get income statement for the stock

        Args:
            ticker (str): the stock ticker to be given to yfinance
        """

        stock = yf.Ticker(ticker)
        income_statement = pd.DataFrame(stock.income_stmt)
        return f"Income Statement:\n{income_statement.to_string()}"
