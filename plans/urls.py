# wallets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet

# Create a router and register the PlanViewSet
router = DefaultRouter()
router.register(r'plans', PlanViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include the router URLs
]
