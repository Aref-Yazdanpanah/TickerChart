from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AverageDailyPriceViewSet,
    TickerPriceChangeViewSet,
    TickerViewSet,
)

router = DefaultRouter()
router.register(
    r"ticker-price-change", TickerPriceChangeViewSet, basename="ticker-price-change"
)
router.register(
    r"average-daily-prices", AverageDailyPriceViewSet, basename="average-daily-prices"
)
router.register(r"tickers", TickerViewSet, basename="tickers")


app_name = "chartengine"
urlpatterns = [
    path("", include(router.urls)),
]
