# accounts/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import UserWallet
from datetime import datetime, timedelta, timezone
from rest_framework.decorators import api_view

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"message": "Login successful", "access_token": access_token})
        return Response({"error": "Invalid credentials"}, status=400)


# accounts/views.py
from rest_framework import status, generics
# from rest_framework.response import Response
from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate

class RegisterAPIView(generics.CreateAPIView):
    model = User
    fields = ['username', 'password', 'email']
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        wallet = UserWallet.objects.create(user=user, balance=50, currency='USD')
        token = Token.objects.create(user=user)
        return Response({"message": "User created", "token": token.key}, status=status.HTTP_201_CREATED)

# accounts/views.py
# from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = UserPlan.objects.filter(user=request.user, status='active')
        serilisedPlan = UserPlanSerializer(plans, many=True)
        if len(plans) > 0:
            plan = plans[0]
            if plan.date_completed is not None and datetime.now(tz=timezone.utc) > plan.date_completed:
                plan.status = 'completed'
                plan.save()

        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "balance": request.user.user_wallet.balance,
            "id": request.user.pk,
            "plans": serilisedPlan.data,
        })


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Plan, UserPlan
from .serializer import UserPlanSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import response

# Plan Views
class PlanListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plan.objects.all()
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]  # Require authentication


class PlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plan.objects.all()
    serializer_class = UserPlanSerializer
    permission_classes = [IsAuthenticated]


# UserPlan Views
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def create_user_plan(request):
    """
    Create a new UserPlan.
    """
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Validate the input
    if not plan_id:
        return Response(
            {"error": "The 'plan' field is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        plans = UserPlan.objects.filter(user= request.user, status='active')
        if len(plans) > 0:
            return Response(
                {"error": "You already have an active plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        plan_id = request.data.get('plan')  # Extract the plan ID from the request data
        wallet = UserWallet.objects.get(user=request.user)

        if wallet.balance < plan.price:
            return Response(
                {"error": "Insufficient balance."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return Response(
            {"error": f"Plan with id {plan_id} does not exist."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate the future date based on the plan's duration
    today = datetime.now(timezone.utc)
    future_date = today + timedelta(days=plan.duration_in_months * 30)  # Approximate months as days

    # Create the UserPlan instance
    user_plan = UserPlan.objects.create(
        user=request.user,
        plan=plan,
        status="active",  # Set the status to active by default
        date_completed=future_date,  # Will be set later
        current_balance=plan.gain,
    )

    # Deduct the plan price from the user's wallet
    wallet.balance -= plan.price
    wallet.save()

    # Return a custom success response
    return Response(
        {
            "message": "User plan created successfully.",
            "data": {
                "id": user_plan.pk,
                "user": user_plan.user.username,
                "plan": {
                    "id": user_plan.plan.pk,
                    "name": user_plan.plan.name,
                },
                "status": user_plan.status,
                "date_completed": user_plan.date_completed,
                "created_at": user_plan.created_at,
                "future_date": future_date,  # Optional, add if needed
            },
        },
        status=status.HTTP_201_CREATED,
    )

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserSerializer, UserWalletSerializer

# class UsersWithWalletView(APIView):
#     def get(self, request):
#         users = User.objects.all()  # Fetch all users
#         # Include the wallet in the response by using the serializer
#         serializer = UserWalletSerializer(users, many=True)
#         return Response(serializer.data)

class UsersWithWalletView(APIView):
    # permission_classes = [IsAuthenticated]  # Optionally, require authentication

    def get(self, request):
        # Fetch all users along with their associated wallet
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)