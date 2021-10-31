from django.contrib import admin
from coinmarketcap.models import *


@admin.register(CoinCapData)
class CoinCapDataAdmin(admin.ModelAdmin):
    list_display = ['website', 'symbol', 'token', 'hosts', 'marketCap']
    list_display_links = ['hosts']


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = [
        'host',
    ]
