# events/serializers.py
from rest_framework import serializers
from .models import CustomerProfile, OrganizerProfile
from .models import Event, TicketPackage, Cart, CartItem, TicketPurchase, QRCode
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

from rest_framework import serializers
from .models import Event, TicketPackage

class TicketPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPackage
        fields = '__all__'

from rest_framework import serializers
from .models import Event, TicketPackage

class TicketPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPackage
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    """ user = serializers.StringRelatedField() """
    ticket_packages = TicketPackageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


# rest of your serializers...

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'event', 'ticket_package', 'quantity']

class CartItemReadSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.eventNAME', read_only=True)
    package_name = serializers.CharField(source='ticket_package.package_name', read_only=True)
    package_price = serializers.DecimalField(source='ticket_package.package_price', max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'event', 'event_name', 'ticket_package', 'package_name','package_price', 'quantity']



class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
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