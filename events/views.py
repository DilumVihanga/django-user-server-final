from django.shortcuts import render
from .models import User,CustomerProfile, OrganizerProfile
from .models import Event, Ticket, TicketPackage, Order, Payment, QRCode
from .serializers import UserSerializer, CustomerProfileSerializer, OrganizerProfileSerializer
from .serializers import EventSerializer, TicketSerializer, TicketPackageSerializer, OrderSerializer, PaymentSerializer, QRCodeSerializer
from rest_framework import viewsets

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