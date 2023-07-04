from django.contrib import admin
from .models import TransactionHistory, Wallet, Network, Coin, Block

admin.site.register(Network)
admin.site.register(Wallet)
admin.site.register(Coin)
admin.site.register(TransactionHistory)
admin.site.register(Block)

