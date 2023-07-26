from django.shortcuts import render
from .models import User,CustomerProfile, OrganizerProfile
from .models import Event, Ticket, TicketType, Order, Payment, QRCode
from .serializers import UserSerializer, CustomerProfileSerializer, OrganizerProfileSerializer
from .serializers import EventSerializer, TicketSerializer, TicketTypeSerializer, OrderSerializer, PaymentSerializer, QRCodeSerializer
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

class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

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

# backend/users/views.py

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrganizerProfileSerializer
from .models import OrganizerProfile

class OrganizerProfileView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizerProfileSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        queryset = OrganizerProfile.objects.filter(user__id=user_id)
        return queryset

       
        
