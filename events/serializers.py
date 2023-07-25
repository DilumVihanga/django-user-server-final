# events/serializers.py
from rest_framework import serializers
from .models import CustomerProfile, OrganizerProfile
from .models import Event, Ticket, TicketType, Order, Payment, QRCode
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['user', 'customerPHONE', 'customerNIC']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.role = User.Role.CUSTOMER  # Set the role after creating the user
        user.save()
        customer_profile = CustomerProfile.objects.create(user=user, **validated_data)
        return customer_profile

class OrganizerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = OrganizerProfile
        fields = ['user',  'organizerPHONE', 'organizerNIC', 'organizerREGNO', 'addressLINE1', 'addressLINE2', 'organizerCITY', 'organizerAGREED']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.role = User.Role.ORGANIZER  # Set the role after creating the user
        user.save()
        organizer_profile = OrganizerProfile.objects.create(user=user, **validated_data)
        return organizer_profile

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'      



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['role'] = self.user.role

        return data        