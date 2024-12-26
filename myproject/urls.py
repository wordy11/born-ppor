# project_name/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallets.urls')),  # Include wallet URLs here
    path('', include('plans.urls')),  # Include plan URLs here
    path('', include('transactions.urls')),  # Include transaction URLs here
    path('', include('users.urls')),  # Include customer URLs here
]

# add at the last
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
