from django.contrib import admin
from django.urls import path
from trc20webhook.views import TransactionHistoryView


urlpatterns = [
    path('create-transaction/', TransactionHistoryView.as_view()),
]

