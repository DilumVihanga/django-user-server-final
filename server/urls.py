from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from events.views import CustomTokenObtainPairView, validate_username_email
from events.views import UserViewSet, CustomerProfileViewSet, OrganizerProfileViewSet , getEventsbyUser
from events.views import EventViewSet, TicketViewSet, TicketPackageViewSet, OrderViewSet, PaymentViewSet, QRCodeViewSet, CartViewSet, CartItemViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('customer-profiles', CustomerProfileViewSet)
router.register('organizer-profiles', OrganizerProfileViewSet)
router.register('events', EventViewSet)
router.register('tickets', TicketViewSet)
router.register('ticket-packages', TicketPackageViewSet)    
router.register('orders', OrderViewSet)
router.register('payments', PaymentViewSet)
router.register('cart', CartViewSet)
router.register('cart-items', CartItemViewSet)
router.register('carts', CartViewSet)
router.register('items', CartItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/validate-username-email/', validate_username_email, name='validate_username_email'),
    path('api/pak/<int:user_id>', getEventsbyUser ,name='rest_framework'),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)