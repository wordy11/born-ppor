# wallets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet

# Create a router and register the WalletViewSet
router = DefaultRouter()
router.register(r'wallets', WalletViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router URLs
]
