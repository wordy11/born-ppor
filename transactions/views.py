from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Transaction
from users.models import UserWallet
from decimal import Decimal

@api_view(['POST'])
def create_transaction(request):
    data = request.data
    wallet_id = data.get('wallet')
    amount = Decimal(data.get('amount'))  # Convert amount to Decimal
    transaction_type = data.get('transaction_type')
    asset_symbol = data.get('asset_symbol')
    asset_name = data.get('asset_name')
    from_address = data.get('from_address')
    to_address = data.get('to_address')
    transaction_hash = data.get('transaction_hash')

    # Check if wallet exists
    try:
        # Fetch wallet by ID (this should be a UserWallet object)
        wallet = UserWallet.objects.get(pk=wallet_id)
    except UserWallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure proper transaction type handling
    if transaction_type == 'deposit':
        wallet.balance += amount  # Increase wallet balance
    elif transaction_type == 'withdrawal':
        if wallet.balance >= amount:
            wallet.balance -= amount  # Decrease wallet balance
        else:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)
    
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

    return Response({'message': 'Transaction successfully created', 'transaction_id': transaction.id}, status=status.HTTP_201_CREATED)
