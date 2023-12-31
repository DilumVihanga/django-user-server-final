from django.shortcuts import render
from .models import User,CustomerProfile, OrganizerProfile
from .models import Event,  TicketPackage, Cart, CartItem, TicketPurchase, QRCode
from .serializers import UserSerializer, CustomerProfileSerializer, OrganizerProfileSerializer, CartItemReadSerializer, TicketPurchaseSerializer
from .serializers import EventSerializer, TicketPackageSerializer,  CartSerializer, CartItemSerializer, QRCodeSerializer
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

class TicketPurchaseViewSet(viewsets.ModelViewSet):
    queryset = TicketPurchase.objects.all()
    serializer_class = TicketPurchaseSerializer

                  
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
        success_url='http://localhost:3000/ordersuccess',
        cancel_url='http://localhost:3000/cart',
    )

    return JsonResponse({'session': {'url': session.url}})


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import TicketPurchase
import json

@csrf_exempt
@require_POST
def save_ticket_purchase(request):
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        event_name = data['event_name']
        package_name = data['package_name']
        package_price = data['package_price']
        quantity = data['quantity']
        subtotal = data['subtotal']

        ticket_purchase = TicketPurchase.objects.create(
            user_id=user_id,
            event_name=event_name,
            package_name=package_name,
            package_price=package_price,
            quantity=quantity,
            subtotal=subtotal
        )

        return JsonResponse({'success': True, 'ticket_purchase_id': ticket_purchase.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


from django.http import JsonResponse
from .models import Event
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_event(request, event_id):
    if request.method == "PUT":
        try:
            event = Event.objects.get(id=event_id)
            event.eventNAME = request.PUT.get('eventNAME', event.eventNAME)
            event.eventDATE = request.PUT.get('eventDATE', event.eventDATE)
            event.eventDISCRIPTION = request.PUT.get('eventDISCRIPTION', event.eventDISCRIPTION)
            event.eventLOCATION = request.PUT.get('eventLOCATION', event.eventLOCATION)
            event.eventSTARTTIME = request.PUT.get('eventSTARTTIME', event.eventSTARTTIME)
            event.eventADDRESS = request.PUT.get('eventADDRESS', event.eventADDRESS)

            # Handle the event image
            if 'eventIMAGE' in request.FILES:
                event.eventIMAGE = request.FILES['eventIMAGE']

            event.save()
            return JsonResponse({'message': 'Event updated successfully'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
from django.http import JsonResponse

def get_ticket_purchase(request, ticket_purchase_id):
    try:
        ticket_purchase = TicketPurchase.objects.get(id=ticket_purchase_id)
        ticket_packages = TicketPackage.objects.filter(ticket_purchase=ticket_purchase)
        packages = [
            {
                'name': package.package_name,
                'description': package.package_description,
                'price': package.package_price,
                'quantity': package.package_ticketquantity,
            }
            for package in ticket_packages
        ]
        return JsonResponse({
            'event_name': ticket_purchase.event_name,
            'subtotal': ticket_purchase.subtotal,
            'purchase_date': ticket_purchase.purchase_date,
            'packages': packages,
        })
    except TicketPurchase.DoesNotExist:
        return JsonResponse({'error': 'Ticket purchase not found'}, status=404)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem

@api_view(['DELETE'])
def clear_cart_for_user(request, user_id):
    try:
        CartItem.objects.filter(cart__user_id=user_id).delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def validate_qr_code(request, qr_code_id):
    try:
        qr_code = QRCode.objects.get(id=qr_code_id)
        qr_code.validated = True
        qr_code.save()
        return Response({'message': 'QR code validated successfully'}, status=200)
    except QRCode.DoesNotExist:
        return Response({'error': 'QR code not found'}, status=404)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserUpdateSerializer  # Adjust the import path as needed

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
