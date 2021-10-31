from django.db import models


class Host(models.Model):
    host = models.CharField(max_length=100, unique=True)


class CoinCapData(models.Model):
    website = models.CharField(max_length=200, primary_key=True)
    symbol = models.CharField(max_length=50)
    token = models.CharField(max_length=100)
    hosts = models.ForeignKey(
        Host,
        on_delete=models.CASCADE
    )
    marketCap = models.IntegerField()
