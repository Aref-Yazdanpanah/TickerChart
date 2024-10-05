from decimal import Decimal

from rest_framework import status, viewsets
from rest_framework.response import Response

from .services import TickerService


class TickerPriceChangeViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            # Extract and parse input data
            (
                tickers_data,
                start_time,
                end_time,
                interval_days,
            ) = TickerService.parse_input_data(request.data)

            # Dictionary to hold final output for aggregated ticker values
            total_value_over_time = {}

            # Loop through each ticker and calculate the values
            for ticker_name, ticker_quantity in tickers_data.items():
                ticker, market_data = TickerService.get_ticker_data(
                    ticker_name, start_time, end_time
                )

                if not ticker:
                    return Response(
                        {"error": f"Ticker {ticker_name} not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Convert ticker_quantity to Decimal
                ticker_quantity = Decimal(str(ticker_quantity))

                # Calculate the ticker value over time
                ticker_value_over_time = TickerService.calculate_ticker_value(
                    market_data, ticker_quantity, start_time, end_time, interval_days
                )

                # Aggregate the total ticker value over time intervals
                for entry in ticker_value_over_time:
                    interval_start = entry["interval_start"]
                    ticker_value = entry["ticker_value"]

                    if interval_start not in total_value_over_time:
                        total_value_over_time[interval_start] = ticker_value
                    else:
                        total_value_over_time[interval_start] += ticker_value

            # Prepare the response data
            response_data = [
                {"interval_start": interval, "total_value": value}
                for interval, value in total_value_over_time.items()
            ]

            return Response(
                {
                    "message": "Total price change data calculated successfully",
                    "data": response_data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error processing data", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
