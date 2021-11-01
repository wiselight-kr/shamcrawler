from django.db import models


class Coin(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=50, null=True)
    ethTokenAddress = models.CharField(max_length=100, null=True)
    bscTokenAddress = models.CharField(max_length=100, null=True)
    marketCap = models.IntegerField(null=True)
    website = models.CharField(max_length=200, null=True)
