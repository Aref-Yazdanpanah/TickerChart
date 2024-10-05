import time
from datetime import datetime

import requests
from django.core.management.base import BaseCommand
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from TickerChart.chartengine.models import MarketData, Ticker


# Function to get historical kline data with retries and save to DB
def get_historical_data(symbol, start_time, end_time):
    BASE_URL = "https://api.binance.com/api/v3/klines"
    data = []

    # Create a session with retries
    session = requests.Session()
    retries = Retry(
        total=5,  # Retry 5 times
        backoff_factor=0.3,  # Wait time between retries (exponential backoff)
        status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP status codes
        allowed_methods=["GET"],  # Retry only on GET requests
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)

    # Fetch or create the Ticker instance
    ticker_instance, created = Ticker.objects.get_or_create(name=symbol)

    while start_time < end_time:
        params = {
            "symbol": symbol,
            "interval": "15m",
            "startTime": start_time,
            "limit": 1000,
        }
        try:
            response = session.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()  # Raise an error for bad responses
            klines = response.json()

            if not klines:
                break

            # Extract and save the relevant data
            for kline in klines:
                close_time_ms = kline[6]
                close_price = kline[4]

                # Convert close_time from milliseconds to datetime
                close_time = datetime.utcfromtimestamp(close_time_ms / 1000.0)

                # Append to the list with symbol
                data.append(
                    {
                        "symbol": symbol,
                        "close_time": close_time,
                        "close_price": close_price,
                    }
                )

                # Save to the database
                MarketData.objects.create(
                    ticker=ticker_instance,  # Use the Ticker instance
                    close=close_price,
                    date=close_time,
                )

            # Update start_time to the last closeTime
            start_time = klines[-1][6]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            break

    return data


def fetch_data_for_all_symbols():
    # Binance API URL for Kline data
    EXCHANGE_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"

    # Set parameters
    start_time = 1704067200000  # January 1, 2024 in milliseconds
    end_time = int(time.time() * 1000)  # Current time in milliseconds

    # Get all symbols
    response = requests.get(EXCHANGE_INFO_URL)
    symbols = [s["symbol"] for s in response.json()["symbols"] if "USDT" in s["symbol"]]

    # Fetch data for all symbols
    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        historical_data = get_historical_data(symbol, start_time, end_time)
        print(f"Fetched {len(historical_data)} records for {symbol}.")


class Command(BaseCommand):
    help = "Fetches historical market data for all symbols from Binance"

    def handle(self, *args, **kwargs):
        try:
            fetch_data_for_all_symbols()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully fetched historical data for all symbols."
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error fetching historical data: {e}"))
