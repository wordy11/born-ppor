# wallets/serializers.py

from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'network', 'address']  # Include fields that should be serialized
