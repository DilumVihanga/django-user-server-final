from django.contrib import admin
from .models import User, Customer, Organizer, CustomerProfile, OrganizerProfile
from .models import Event, Ticket, TicketPackage, QRCode

# Register your models here.

admin.site.register(User)
admin.site.register(CustomerProfile)
admin.site.register(OrganizerProfile)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(TicketPackage)
admin.site.register(QRCode)



admin.sitename = 'Event Management System'

