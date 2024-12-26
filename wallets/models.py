# Create your models here.
# wallets/models.py

from django.db import models

class Wallet(models.Model):
    name = models.CharField(max_length=255)
    network = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
