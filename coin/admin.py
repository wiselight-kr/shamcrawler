from django.contrib import admin
from coin.models import *


@admin.register(Coin)
class CoinCapDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'ethTokenAddress', 'bscTokenAddress', 'marketCap', 'website']

