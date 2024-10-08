from decimal import Decimal

from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .models import Ticker
from .pagination import TickerPagination
from .schemas import average_daily_prices, ticker_price_change, tickers_list
from .serializers import TickerSerializer
from .services import TickerService


class TickerPriceChangeViewSet(viewsets.ViewSet):
    @ticker_price_change
    def list(self, request):
        try:
            # Extract and parse input data
            (
                tickers_data,
                start_time,
                end_time,
                interval_days,
            ) = TickerService.parse_input_data(request.data)

            # Get ticker names and corresponding IDs
            ticker_names = list(tickers_data.keys())
            tickers = TickerService.get_tickers_data(ticker_names)
            ticker_ids = [ticker.id for ticker in tickers.values()]

            # Dictionary to hold final output
            output = {}

            # Fetch all market data for the relevant tickers in one query
            market_data = TickerService.get_market_data(
                ticker_ids, start_time, end_time
            )

            # Group market data by ticker ID for processing
            grouped_market_data = {}
            for md in market_data:
                if md.ticker_id not in grouped_market_data:
                    grouped_market_data[md.ticker_id] = []
                grouped_market_data[md.ticker_id].append(md)

            # Loop through each ticker and calculate the values
            for ticker_name, ticker_quantity in tickers_data.items():
                ticker = tickers.get(ticker_name)

                if not ticker:
                    return Response(
                        {"error": f"Ticker {ticker_name} not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Convert ticker_quantity to Decimal
                ticker_quantity = Decimal(str(ticker_quantity))

                # Get the market data for the ticker
                ticker_market_data = grouped_market_data.get(ticker.id, [])

                # Calculate the ticker value over time
                ticker_value_over_time = TickerService.calculate_ticker_value(
                    ticker_market_data,
                    ticker_quantity,
                    start_time,
                    end_time,
                    interval_days,
                )

                # Append results to output
                output[ticker_name] = ticker_value_over_time

            return Response(
                {
                    "message": "Price change data calculated successfully",
                    "data": output,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error processing data", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AverageDailyPriceViewSet(viewsets.ViewSet):
    """
    ViewSet to retrieve average daily prices of tickers within a time range.
    """

    @average_daily_prices
    def list(self, request):
        try:
            # Parse request data
            tickers_data, start_time, end_time, _ = TickerService.parse_input_data(
                request.data
            )

            # Get the tickers data from the request
            tickers = TickerService.get_tickers_data(tickers_data)
            if not tickers:
                return Response(
                    {"detail": "No tickers found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get market data for the tickers within the specified time range
            ticker_ids = [ticker.id for ticker in tickers.values()]
            market_data = TickerService.get_market_data(
                ticker_ids, start_time, end_time
            )

            # Calculate average daily prices
            avg_daily_prices = TickerService.calculate_average_daily_prices(market_data)

            # Prepare response data
            response_data = [
                {
                    "ticker_name": record["ticker__name"],
                    "day": record["day"],
                    "average_price": record["avg_price"],
                }
                for record in avg_daily_prices
            ]

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@tickers_list
class TickerListView(generics.ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    pagination_class = TickerPagination
