# wallets/models.py

from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_months = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    gain = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name
