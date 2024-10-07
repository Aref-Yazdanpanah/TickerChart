from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.db.models import Avg
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

        # Group market data into a dictionary based on the intervals
        interval_data_dict = {}
        while current_time < end_time:
            next_time = current_time + timedelta(days=interval_days)
            interval_data_dict[current_time] = [
                md for md in market_data if current_time <= md.date < next_time
            ]
            current_time = next_time

        # Iterate over the grouped intervals and calculate the value based on the last close price
        for interval_start, data_in_interval in interval_data_dict.items():
            if data_in_interval:
                last_close_price = data_in_interval[-1].close
            else:
                last_close_price = Decimal("0")
            ticker_value = last_close_price * ticker_quantity
            total_value_over_time.append(
                {"interval_start": interval_start, "ticker_value": ticker_value}
            )

        return total_value_over_time

    @staticmethod
    def get_tickers_data(ticker_names):
        # Fetch all tickers in one query
        tickers = Ticker.objects.filter(name__in=ticker_names)
        return {ticker.name: ticker for ticker in tickers}

    @staticmethod
    def get_market_data(ticker_ids, start_time, end_time):
        # Fetch all market data for the specified ticker IDs in one query
        return MarketData.objects.filter(
            ticker_id__in=ticker_ids, date__gte=start_time, date__lte=end_time
        ).order_by("ticker_id", "date")

    @staticmethod
    def calculate_average_daily_prices(market_data):
        """
        Calculate average daily prices for the provided market data.
        """
        daily_averages = (
            market_data.annotate(day=models.functions.TruncDay("date"))
            .values("ticker__name", "day")
            .annotate(avg_price=Avg("close"))
            .order_by("ticker__name", "day")
        )
        return daily_averages
