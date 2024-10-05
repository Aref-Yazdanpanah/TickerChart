import requests
from django.core.management.base import BaseCommand

from TickerChart.chartengine.models import Ticker


class Command(BaseCommand):
    help = "Fetch all symbols from Binance and save them to the Ticker model"

    def handle(self, *args, **kwargs):
        EXCHANGE_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"

        # Fetch symbols from Binance
        try:
            response = requests.get(EXCHANGE_INFO_URL)
            response.raise_for_status()  # Raise an exception for bad responses
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching symbols: {e}"))
            return

        # Extract symbols that contain 'USDT'
        symbols = [s["symbol"] for s in data["symbols"] if "USDT" in s["symbol"]]

        # Save each symbol in the Ticker model
        for symbol in symbols:
            ticker, created = Ticker.objects.get_or_create(name=symbol)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Ticker {symbol} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Ticker {symbol} already exists"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully fetched and saved {len(symbols)} symbols."
            )
        )
