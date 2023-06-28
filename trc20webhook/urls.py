from django.contrib import admin
from django.urls import path
from trc20webhook.views import TransactionHistoryView, RegisterWalletView


urlpatterns = [
    path('register-wallet/', RegisterWalletView.as_view()),
    path('create-transaction/', TransactionHistoryView.as_view()),
]

