from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from events.views import CustomTokenObtainPairView, validate_username_email
from events.views import UserViewSet, CustomerProfileViewSet, OrganizerProfileViewSet , getEventsbyUser
from events.views import EventViewSet,  TicketPackageViewSet, CartViewSet, CartItemViewSet, TicketPurchaseViewSet, QRCodeViewSet
from events.views import save_ticket_purchase
from events.views import update_event
from events.views import get_ticket_purchase
from events import views

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('customer-profiles', CustomerProfileViewSet)
router.register('organizer-profiles', OrganizerProfileViewSet)
router.register('events', EventViewSet)

router.register('ticket-packages', TicketPackageViewSet)    

router.register('cart', CartViewSet)
router.register('cart-items', CartItemViewSet)
router.register('carts', CartViewSet)
router.register('items', CartItemViewSet)
router.register('ticket-purchases', TicketPurchaseViewSet)
router.register('qr-codes', QRCodeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/validate-username-email/', validate_username_email, name='validate_username_email'),
    path('api/pak/<int:user_id>', getEventsbyUser ,name='rest_framework'),

    path('api/create-checkout-session', views.create_checkout_session),
    path('api/save-ticket-purchase', save_ticket_purchase, name='save_ticket_purchase'),
    path('api/events/<int:event_id>/', update_event),path('api/ticket_purchase/<int:ticket_purchase_id>/', get_ticket_purchase),



    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)