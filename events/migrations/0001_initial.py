# Generated by Django 4.2.3 on 2023-07-28 19:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("ADMIN", "Admin"),
                            ("CUSTOMER", "Customer"),
                            ("ORGANIZER", "Organizer"),
                        ],
                        max_length=50,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomerProfile",
            fields=[
                ("customerID", models.AutoField(primary_key=True, serialize=False)),
                ("customerPHONE", models.CharField(max_length=20)),
                ("customerNIC", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("eventID", models.AutoField(primary_key=True, serialize=False)),
                ("eventNAME", models.CharField(max_length=200)),
                ("eventDATE", models.DateField()),
                ("eventDISCRIPTION", models.TextField()),
                ("eventLOCATION", models.CharField(max_length=200)),
                ("eventSTARTTIME", models.TimeField()),
                ("eventADDRESS", models.CharField(max_length=200)),
                ("eventIMAGE", models.ImageField(upload_to="uploads/images/")),
                (
                    "eventLAN",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "eventLON",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrganizerProfile",
            fields=[
                ("organizerID", models.AutoField(primary_key=True, serialize=False)),
                ("organizerREGNO", models.CharField(max_length=200)),
                ("organizerPHONE", models.CharField(max_length=20)),
                ("organizerNIC", models.CharField(max_length=20)),
                ("addressLINE1", models.CharField(default="", max_length=200)),
                ("addressLINE2", models.CharField(default="", max_length=200)),
                ("organizerCITY", models.CharField(default="", max_length=200)),
                ("organizerAGREED", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QRCode",
            fields=[
                ("qrcodeID", models.AutoField(primary_key=True, serialize=False)),
                ("qrDATA", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="SalesDashboard",
            fields=[
                ("dashboardID", models.AutoField(primary_key=True, serialize=False)),
                ("topSellingEvents", models.TextField()),
                ("totalRevenue", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "organizerID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.organizerprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicketPackage",
            fields=[
                ("packageID", models.AutoField(primary_key=True, serialize=False)),
                ("package_name", models.CharField(max_length=200)),
                ("package_description", models.TextField()),
                ("package_price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("package_ticketquantity", models.IntegerField()),
                (
                    "eventID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_packages",
                        to="events.event",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("ticketID", models.AutoField(primary_key=True, serialize=False)),
                ("ticket_type", models.CharField(max_length=200)),
                ("ticket_quantity", models.IntegerField()),
                ("ticket_price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("ticket_description", models.TextField()),
                (
                    "packageID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="events.ticketpackage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SalesReport",
            fields=[
                ("reportID", models.AutoField(primary_key=True, serialize=False)),
                ("nic", models.CharField(max_length=20)),
                ("fullName", models.CharField(max_length=200)),
                ("ticketT_NAME", models.CharField(max_length=200)),
                ("ticketQUANTITY", models.IntegerField()),
                ("ticketSUBTOTAL", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "dashboardID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.salesdashboard",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("paymentID", models.AutoField(primary_key=True, serialize=False)),
                ("paymentSTATUS", models.CharField(max_length=200)),
                ("fullName", models.CharField(max_length=200)),
                ("address", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=20)),
                ("nic", models.CharField(max_length=20)),
                (
                    "customerID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.customerprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("orderID", models.AutoField(primary_key=True, serialize=False)),
                ("orderAMOUNT", models.DecimalField(decimal_places=2, max_digits=7)),
                ("orderTIME", models.DateTimeField(auto_now_add=True)),
                ("orderSTATUS", models.CharField(max_length=200)),
                ("orderDATE", models.DateField()),
                (
                    "customerID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.customerprofile",
                    ),
                ),
                (
                    "paymentID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.payment"
                    ),
                ),
                (
                    "qrcodeID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.qrcode"
                    ),
                ),
                (
                    "ticketID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.ticket"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="events.cart",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.event"
                    ),
                ),
                (
                    "ticket_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.ticketpackage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("events.user",),
            managers=[
                ("customers", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Organizer",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("events.user",),
            managers=[
                ("organizer", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
