from rest_framework import serializers
from .models import UserPlan, UserWallet
from django.contrib.auth.models import User

class UserPlanSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = UserPlan


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        # fields = ['id', 'balance', 'currency', 'created_at', 'updated_at']  # Include 'id'
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_wallet = UserWalletSerializer()  # Nested wallet data

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_wallet'] 