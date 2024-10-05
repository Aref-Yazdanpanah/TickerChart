from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TickerPriceChangeViewSet

router = DefaultRouter()
router.register(
    r"ticker-price-change", TickerPriceChangeViewSet, basename="ticker-price-change"
)


app_name = "chartengine"
urlpatterns = [
    path("", include(router.urls)),
]
