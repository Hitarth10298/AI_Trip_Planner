import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> str:
    """Converts an amount from one currency to another using Alpha Vantage API."""
    os.environ['ALPHAVANTAGE_API_KEY'] = os.getenv("ALPHAVANTAGE_API_KEY")
    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response.get['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return value * float(exchange_rate)