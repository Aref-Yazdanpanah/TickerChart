from django.db import models
from django.utils import timezone


class Ticker(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MarketData(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    close = models.DecimalField(max_digits=20, decimal_places=8)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.date and timezone.is_naive(self.date):
            self.date = timezone.make_aware(self.date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker.name} - {self.date}"
