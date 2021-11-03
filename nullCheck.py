import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donghadongha.settings")
import django
django.setup()
from coin.models import Coin

cnt = 0
for coin in Coin.objects.all():
    if coin.marketCap:
        print(coin.symbol)
    else:
        cnt+=1
print(cnt)