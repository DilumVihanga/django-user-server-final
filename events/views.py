from django.shortcuts import render
from .models import User,CustomerProfile, OrganizerProfile
from .models import Event, Ticket, TicketPackage, Order, Payment, QRCode, Cart, CartItem
from .serializers import UserSerializer, CustomerProfileSerializer, OrganizerProfileSerializer, CartItemReadSerializer
from .serializers import EventSerializer, TicketSerializer, TicketPackageSerializer, OrderSerializer, PaymentSerializer, QRCodeSerializer, CartSerializer, CartItemSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class OrganizerProfileViewSet(viewsets.ModelViewSet):
    queryset = OrganizerProfile.objects.all()
    serializer_class = OrganizerProfileSerializer
    
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketPackageViewSet(viewsets.ModelViewSet):
    queryset = TicketPackage.objects.all()
    serializer_class = TicketPackageSerializer    

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# rest of your viewsets...

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CartItemReadSerializer
        return CartItemSerializer

    @action(detail=False, url_path='cart/(?P<cart_id>\d+)', methods=['get'])
    def items_for_cart(self, request, cart_id=None):
        items = self.get_queryset().filter(cart__id=cart_id)
        serializer = CartItemReadSerializer(items, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer                    


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def validate_username_email(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)

    data = {}

    if username:
        existing_usernames = User.objects.filter(username=username)
        data['username_taken'] = existing_usernames.exists()
    
    if email:
        existing_emails = User.objects.filter(email=email)
        data['email_taken'] = existing_emails.exists()

    return Response(data)

@api_view(['GET'])
def getEventsbyUser(request , user_id):
    events = Event.objects.filter(user=user_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def create_checkout_session(request):
    stripe.api_key = 'sk_test_51NZAWGH8EMA77BE5sZT7wQfCTg3ogscDUwQqFCMGeMdV8OCBzzAd0UmvzoPPBVnh5F0zkAYlnVudgnIqgQWQhW4D00XXUtZpND'

    # Parse the request body to get the amount
    body = json.loads(request.body)
    amount = body.get('amount', 1000)  # Example amount in cents

    # Create the checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # Change currency if needed
                'product_data': {
                    'name': 'Ticket Purchase',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:3000/',
        cancel_url='http://localhost:3000/cart',
    )

    return JsonResponse({'session': {'url': session.url}})
