from django.db import models
from django.conf import settings  # This allows for referencing the user model
from django.contrib.auth import get_user_model
from plans.models import Plan

User = get_user_model()  # This gets your custom user model (or default User model if not custom)

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user.username} - Balance: {self.balance} {self.currency}"

    # Optional: Method to add funds to the wallet
    def add_funds(self, amount):
        if amount > 0:
            self.balance += amount
            self.save()

    # Optional: Method to withdraw funds from the wallet
    def withdraw_funds(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient funds or invalid amount")

class UserPlan(models.Model):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='user_plans')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_completed = models.DateTimeField(null=True, blank=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
