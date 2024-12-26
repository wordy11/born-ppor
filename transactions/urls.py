# wallets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, create_transaction, get_transactions_for_wallet

# Create a router and register the TransactionViewSet
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router URLs
    path('api/create-transaction/', create_transaction, name='create-transaction'),
    path('api/wallet/transactions/', get_transactions_for_wallet, name='transaction-list'),
]
