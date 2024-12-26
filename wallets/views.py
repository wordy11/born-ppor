

# Create your views here.
# wallets/views.py

from rest_framework import viewsets
from .models import Wallet
from .serializer import WalletSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
