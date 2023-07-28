from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        ORGANIZER = "ORGANIZER", "Organizer"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    is_active = models.BooleanField(default=True)    

class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER

    customers = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for customers"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customerID = models.AutoField(primary_key=True)
    customerPHONE = models.CharField(max_length=20)
    customerNIC = models.CharField(max_length=20)      


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user=instance)        


class OrganizerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ORGANIZER)

class Organizer(User):
    base_role = User.Role.ORGANIZER

    organizer = OrganizerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for organizers"


class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """ organizerNAME = models.CharField(max_length=200, blank=True, null=True) """
    organizerID = models.AutoField(primary_key=True)
    organizerREGNO = models.CharField(max_length=200)
    organizerPHONE = models.CharField(max_length=20)
    organizerNIC = models.CharField(max_length=20)
    """ organizerIMAGE = models.ImageField(upload_to='uploads/images/') """
    addressLINE1 = models.CharField(max_length=200, default='')
    addressLINE2 = models.CharField(max_length=200, default='')
    organizerCITY = models.CharField(max_length=200, default='')
    organizerAGREED = models.BooleanField(default=False)    


@receiver(post_save, sender=Organizer)
def create_organizer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ORGANIZER":
        OrganizerProfile.objects.create(user=instance)        


class Event(models.Model):
    eventID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventNAME = models.CharField(max_length=200)
    eventDATE = models.DateField()
    eventDISCRIPTION = models.TextField()
    eventLOCATION = models.CharField(max_length=200)
    eventSTARTTIME = models.TimeField()
    eventADDRESS = models.CharField(max_length=200)
    eventIMAGE = models.ImageField(upload_to='uploads/images/')
    eventLAN = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    eventLON = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.eventNAME

class TicketPackage(models.Model):
    packageID = models.AutoField(primary_key=True)
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_packages')
    package_name = models.CharField(max_length=200)
    package_description = models.TextField()
    package_price = models.DecimalField(max_digits=7, decimal_places=2)
    package_ticketquantity = models.IntegerField()

    def __str__(self):
        return self.package_name



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_package = models.ForeignKey(TicketPackage, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    packageID = models.ForeignKey(TicketPackage, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=200)
    ticket_quantity = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=7, decimal_places=2)
    ticket_description = models.TextField()

    def __str__(self):
        return f"{self.packageID.package_name} - {self.ticket_type}"


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    customerID = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE)
    paymentID = models.ForeignKey('Payment', on_delete=models.CASCADE)
    ticketID = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    qrcodeID = models.ForeignKey('QRCode', on_delete=models.CASCADE)
    orderAMOUNT = models.DecimalField(max_digits=7, decimal_places=2)
    orderTIME = models.DateTimeField(auto_now_add=True)
    orderSTATUS = models.CharField(max_length=200)
    orderDATE = models.DateField()

    def __str__(self):
        return str(self.orderID)


class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    customerID = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE)
    paymentSTATUS = models.CharField(max_length=200)
    fullName = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    nic = models.CharField(max_length=20)

    def __str__(self):
        return str(self.paymentID)


class QRCode(models.Model):
    qrcodeID = models.AutoField(primary_key=True)
    qrDATA = models.CharField(max_length=200)

    def __str__(self):
        return str(self.qrcodeID)


class SalesDashboard(models.Model):
    dashboardID = models.AutoField(primary_key=True)
    organizerID = models.ForeignKey('OrganizerProfile', on_delete=models.CASCADE)
    topSellingEvents = models.TextField()
    totalRevenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.dashboardID)


class SalesReport(models.Model):
    reportID = models.AutoField(primary_key=True)
    dashboardID = models.ForeignKey('SalesDashboard', on_delete=models.CASCADE)
    nic = models.CharField(max_length=20)
    fullName = models.CharField(max_length=200)
    ticketT_NAME = models.CharField(max_length=200)
    ticketQUANTITY = models.IntegerField()
    ticketSUBTOTAL = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.reportID)
