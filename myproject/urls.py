# project_name/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallets.urls')),  # Include wallet URLs here
    path('', include('plans.urls')),  # Include plan URLs here
    path('', include('transactions.urls')),  # Include transaction URLs here
    path('', include('users.urls')),  # Include customer URLs here
]
