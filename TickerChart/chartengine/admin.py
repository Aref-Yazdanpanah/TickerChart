from django.contrib import admin

from .models import MarketData, Ticker

admin.site.register(Ticker)
admin.site.register(MarketData)
