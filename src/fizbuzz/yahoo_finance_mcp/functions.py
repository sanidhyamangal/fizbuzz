from enum import Enum

import pandas as pd
import yfinance as yf
from pydantic import BaseModel


class StockInput(BaseModel):
    ticker: str


class StockToolList(str, Enum):
    BASIC_STOCK_INFORMATION = "basic_stock_information"
    STOCK_NEWS = "stock_news"
    ANALYST_RECOMMENDATIONS = "analyst_recommendations"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"
    INCOME_STATEMENT = "income_statement"


class StockTools:
    @classmethod
    def balance_sheet(cls, ticker: str) -> str:
        """A function to download balance sheet from yahoo finance for a given ticker

        Args:
            ticker (str): A stock ticker to be given to yahoo finance

        Returns:
            str: balance sheet of given stock ticker
        """

        stock = yf.Ticker(ticker=ticker)
        balance_sheet = pd.DataFrame(stock.balance_sheet)
        return f"Balance Sheet:\n{balance_sheet.to_string()}"

    @classmethod
    def cash_flow(cls, ticker: str) -> str:
        """A function to return chashflow of a stock from yahoo finance

        Args:
            ticker (str): A stock ticker to be given to yahoo finance

        Returns:
            str: cash flow of a given stock ticker
        """

        stock = yf.Ticker(ticker=ticker)
        cash_flow = pd.DataFrame(stock.cash_flow)
        return f"Cash Flow:\n{cash_flow.to_string()}"

    @classmethod
    def basic_stock_information(cls, ticker: str) -> str:
        """A function to return basic stock information. Eg. price, description, name

        Args:
            ticker (str): A stock ticker to be given to yahoo finance

        Returns:
            str: basic stock information of a given stock
        """

        stock = yf.Ticker(ticker=ticker)
        return f"Basic Stock information:\n{stock.info}"

    @classmethod
    def analyst_recommendations(cls, ticker: str) -> str:
        """Get the analyst recommendations for the stocks

        Args:
            ticker (str): the stock ticker to be given to yfinance

        Returns:
            str: analyst recommendations for the given stock ticker
        """
        stock = yf.Ticker(ticker)
        return f"Recommendations:\n{stock.recommendations}"

    @classmethod
    def stock_news(cls, ticker: str) -> str:
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

    @classmethod
    def income_statement(cls, ticker: str) -> str:
        """Get income statement for the stock

        Args:
            ticker (str): the stock ticker to be given to yfinance

        Returns:
            str: income statement for the given stock ticker
        """

        stock = yf.Ticker(ticker)
        income_statement = pd.DataFrame(stock.income_stmt)
        return f"Income Statement:\n{income_statement.to_string()}"
