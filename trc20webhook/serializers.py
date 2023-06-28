from rest_framework import serializers
from trc20webhook.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'


class RegisterWalletSerializer(serializers.Serializer):
    wallet = serializers.CharField()
    network = serializers.CharField()
