from rest_framework.views import APIView
from rest_framework.response import Response
from trc20webhook.models import TransactionHistory
from trc20webhook.serializers import TransactionHistorySerializer, RegisterWalletSerializer


class TransactionHistoryView(APIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer

