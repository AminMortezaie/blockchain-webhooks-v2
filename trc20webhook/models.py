from django.db import models
from django.contrib.auth.admin import User
from django.db import IntegrityError
from datetime import datetime
import base58


class BaseModel(models.Model):
    name = models.CharField(max_length=250, blank=False)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def soft_delete(self):
        if self.is_active:
            self.is_active = False
            self.save()

    class Meta:
        abstract = True


class Network(BaseModel):
    WEB3 = 'WB3'
    BTCFORK = 'BTC'
    API = 'API'
    TYPE_CHOICES = ((WEB3, 'Web3'),
                    (BTCFORK, 'BtcFork'),
                    (API, 'API'),)
    symbol = models.CharField(max_length=8, blank=False)
    deposit_enabled = models.BooleanField(default=False)
    withdrawal_enabled = models.BooleanField(default=False)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)


class Wallet(BaseModel):
    address = models.CharField(max_length=250)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class Coin(BaseModel):
    NATIVE = 'NTV'
    CONTRACT = 'CNT'
    TYPE_CHOICES = ((NATIVE, 'Native'),
                    (CONTRACT, 'Contract'),)
    decimals = models.IntegerField(verbose_name='decimals')
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    contract_address = models.CharField(max_length=100, blank=True)
    abi = models.TextField(blank=True)
    parse = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)


class Block(models.Model):
    last_block_number = models.IntegerField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class TransactionHistory(models.Model):
    block_number = models.CharField(max_length=100, null=True)
    transaction_hash = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default='')
    transaction_type = models.CharField(default="withdrawal", max_length=10)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'transaction_history_{wallet_id}'
        unique_together = ('transaction_hash', 'network',)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            pass

    def __str__(self):
        return self.transaction_hash










