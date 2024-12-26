# wallets/views.py

from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Transaction
from users.models import UserWallet

@api_view(['POST'])
def create_transaction(request):
    data = request.data
    # Extract form data
    wallet_id = data.get('wallet')
    amount = Decimal(data.get('amount'))  # Convert amount to Decimal
    transaction_type = data.get('transaction_type')
    asset_symbol = data.get('asset_symbol')
    asset_name = data.get('asset_name')
    from_address = data.get('from_address')
    to_address = data.get('to_address')
    transaction_hash = data.get('transaction_hash')

        # Fetch wallet by ID (this should be a UserWallet object)
    wallet = UserWallet.objects.get(id=wallet_id)

        # Ensure proper transaction type handling
    if transaction_type == 'deposit':
        wallet.balance += amount  # Increase wallet balance
    elif transaction_type == 'withdrawal':
        if wallet.balance >= amount:
            wallet.balance -= amount  # Decrease wallet balance
        else:
            return Response({'error': 'Insufficient funds'}, status=400)
    else:
        return Response({'error': 'Invalid transaction type'}, status=400)
    wallet.save()

        # Create the transaction record
    transaction = Transaction.objects.create(
            wallet=wallet,  # This is now correctly referencing a UserWallet instance
            amount=amount,
            transaction_type=transaction_type,
            asset_symbol=asset_symbol,
            asset_name=asset_name,
            from_address=from_address,
            to_address=to_address,
            transaction_hash=transaction_hash
        )
    
    

    return Response({'message': 'Transaction successfully created', 'transaction_id': transaction.id}, status=201)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction, UserWallet
from .serializers import TransactionSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_transactions_for_wallet(request):
    try:
        # Fetch the user's wallet using request.user
        wallet = UserWallet.objects.get(user=request.user)

        # Fetch all transactions associated with this wallet
        transactions = Transaction.objects.filter(wallet=wallet)

        # Serialize the transaction data
        serializer = TransactionSerializer(transactions, many=True)

        # Return serialized data
        return Response({'transactions': serializer.data}, status=200)

    except UserWallet.DoesNotExist:
        return Response({'error': 'Wallet not found for the logged-in user'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
