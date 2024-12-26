# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserDetailsAPIView, create_user_plan, UsersWithWalletView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user-details/', UserDetailsAPIView.as_view(), name='user-details'),
    path('user-plans/', create_user_plan, name='user-plans'),
    path('users-with-wallet/', UsersWithWalletView.as_view(), name='users-with-wallet'),
]
