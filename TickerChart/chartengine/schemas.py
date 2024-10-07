from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import TickerSerializer

ticker_price_change = extend_schema(
    description="Calculate price change data for a list of tickers over time",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "object",
                    "description": "Dictionary of ticker symbols and their quantities",
                    "additionalProperties": {"type": "number"},
                    "example": {"BTCUSDT": 2, "ETHUSDT": 3.2, "BBUSDT": 2.1},
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Start time for the price change calculation",
                    "example": "2024-07-01T00:00:00",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "End time for the price change calculation",
                    "example": "2024-10-01T00:00:00",
                },
                "interval_time": {
                    "type": "string",
                    "description": 'Interval time for the calculations (e.g., "1 days")',
                    "example": "1 days",
                },
            },
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Price change data calculated successfully",
                },
                "data": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "interval_start": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2024-07-01T00:00:00Z",
                                },
                                "ticker_value": {
                                    "type": "number",
                                    "example": 125799.98,
                                },
                            },
                        },
                    },
                },
            },
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Ticker BTCUSDT not found"}
            },
        },
        500: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Error processing data"},
                "error": {"type": "string", "example": "Exception message details"},
            },
        },
    },
)


average_daily_prices = extend_schema(
    description="Retrieve average daily prices of tickers within a specific time range",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {"type": "string", "example": "BTCUSDT"},
                    "description": "List of tickers to retrieve average prices for",
                    "example": ["BTCUSDT", "ETHUSDT"],
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Start time for the average price calculation",
                    "example": "2024-01-01T00:00:00Z",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "End time for the average price calculation",
                    "example": "2024-01-31T23:59:59Z",
                },
            },
        }
    },
    responses={
        200: {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ticker_name": {"type": "string", "example": "BTCUSDT"},
                    "day": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2024-01-01T00:00:00Z",
                    },
                    "average_price": {"type": "number", "example": 42809.511666666665},
                },
            },
        },
        400: {
            "type": "object",
            "properties": {
                "detail": {"type": "string", "example": "Error message details"}
            },
        },
        404: {
            "type": "object",
            "properties": {
                "detail": {"type": "string", "example": "No tickers found."}
            },
        },
    },
)


tickers_list = extend_schema(
    description="Retrieve a paginated list of tickers",
    parameters=[
        OpenApiParameter(
            name="page",
            description="A page number within the paginated result set.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="page_size",
            description="Number of results to return per page.",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: TickerSerializer(many=True),
        400: {
            "type": "object",
            "properties": {"detail": {"type": "string", "example": "Error message"}},
        },
    },
)
