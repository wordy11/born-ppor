# wallets/models.py

from django.db import models
from users.models import UserWallet

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    )

    # Reference to Wallet model in 'wallets' app
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)  # Cryptocurrency amounts with high precision
    asset_name = models.CharField(max_length=50)  # e.g., Bitcoin, Ethereum, etc.
    asset_symbol = models.CharField(max_length=10)  # e.g., BTC, ETH
    from_address = models.CharField(max_length=255, blank=True, null=True)  # Sender's address, optional
    to_address = models.CharField(max_length=255, blank=True, null=True)  # Receiver's address, optional
    transaction_hash = models.CharField(max_length=255, unique=True)  # Transaction hash (tx hash)
    status = models.CharField(max_length=20, default='pending')  # Status of the transaction
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of transaction creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.asset_name} - {self.amount}"

    class Meta:
        ordering = ['-created_at']  # Order by creation date (latest first)
