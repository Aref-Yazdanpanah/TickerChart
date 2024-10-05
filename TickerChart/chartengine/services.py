from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import MarketData, Ticker


class TickerService:
    @staticmethod
    def parse_input_data(request_data):
        tickers_data = request_data.get("tickers")
        start_time = parse_datetime(request_data.get("start_time"))
        end_time = parse_datetime(request_data.get("end_time"))

        # Ensure the datetime is timezone-aware
        if start_time and timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)
        if end_time and timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time)

        interval_time = request_data.get("interval_time", "1 days")
        interval_days = int(interval_time.split()[0])
        return tickers_data, start_time, end_time, interval_days

    @staticmethod
    def calculate_ticker_value(
        market_data, ticker_quantity, start_time, end_time, interval_days
    ):
        current_time = start_time
        total_value_over_time = []

        while current_time < end_time:
            next_time = current_time + timedelta(days=interval_days)

            # Get the last close price in this interval
            interval_data = market_data.filter(
                date__gte=current_time, date__lt=next_time
            ).order_by("date").last()

            last_close_price = interval_data.close if interval_data else Decimal("0")
            ticker_value = last_close_price * ticker_quantity

            total_value_over_time.append(
                {"interval_start": current_time, "ticker_value": ticker_value}
            )

            current_time = next_time

        return total_value_over_time

    @staticmethod
    def get_ticker_data(ticker_name, start_time, end_time):
        try:
            ticker = Ticker.objects.get(name=ticker_name)
            market_data = MarketData.objects.filter(
            # market_data = MarketData.objects.select_related('ticker').filter(
                ticker=ticker, date__gte=start_time, date__lte=end_time
            ).order_by("date")
            return ticker, market_data
        except Ticker.DoesNotExist:
            return None, None
