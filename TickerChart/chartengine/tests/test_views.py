from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from TickerChart.chartengine.models import MarketData, Ticker


class TickerListViewTests(APITestCase):
    def setUp(self):
        Ticker.objects.create(name="Bitcoin")
        Ticker.objects.create(name="Ethereum")

    def test_list_tickers(self):
        # Define the URL for the ticker list view
        url = reverse(
            "chartengine:tickers-list"
        )

        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the response data
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Bitcoin")
        self.assertEqual(response.data["results"][1]["name"], "Ethereum")


class TickerPriceChangeViewSetTests(APITestCase):
    def setUp(self):
        self.ticker1 = Ticker.objects.create(name="Bitcoin")
        self.ticker2 = Ticker.objects.create(name="Ethereum")

        # Create test market data with aware datetime
        MarketData.objects.create(
            ticker=self.ticker1,
            close=Decimal("45000.00"),
            date=timezone.make_aware(timezone.datetime(2024, 10, 1, 12, 0)),
        )
        MarketData.objects.create(
            ticker=self.ticker2,
            close=Decimal("3000.00"),
            date=timezone.make_aware(timezone.datetime(2024, 10, 1, 12, 0)),
        )

    def test_create_price_change_success(self):
        url = reverse("chartengine:ticker-price-change-list")

        # Sample request data
        request_data = {
            "tickers": {
                "Bitcoin": 1,
                "Ethereum": 2,
            },
            "start_time": "2024-10-01T00:00:00Z",
            "end_time": "2024-10-02T00:00:00Z",
            "interval_time": "1 days",
        }

        # Make the POST request
        response = self.client.post(url, request_data, format="json")

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the expected data structure
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)

        # Additional checks based on your business logic
        self.assertEqual(
            response.data["message"], "Price change data calculated successfully"
        )
        self.assertIn("Bitcoin", response.data["data"])
        self.assertIn("Ethereum", response.data["data"])

    def test_create_price_change_ticker_not_found(self):
        url = reverse("chartengine:ticker-price-change-list")

        # Sample request data with a non-existent ticker
        request_data = {
            "tickers": {
                "NonExistentTicker": 1,
            },
            "start_time": "2024-10-01T00:00:00Z",
            "end_time": "2024-10-02T00:00:00Z",
            "interval_time": "1 days",
        }

        response = self.client.post(url, request_data, format="json")

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check that the response contains the expected error message
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Ticker NonExistentTicker not found")

    def tearDown(self):
        # Clean up any objects created during testing if necessary
        Ticker.objects.all().delete()
        MarketData.objects.all().delete()
