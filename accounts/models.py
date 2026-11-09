import random
import string
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Remove username field completely
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    class RoleChoices(models.TextChoices):
        USER = 'USER', _('Normal User')
        ADMIN = 'ADMIN', _('Admin')

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        help_text=_("Designates the user's primary access level.")
    )

    # 6-Character Alphanumeric OTP fields
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No username required

    objects = CustomUserManager()

    def generate_otp(self):
        """Generates a random 6-character alphanumeric OTP valid for 10 minutes."""
        characters = string.ascii_uppercase + string.digits
        self.otp_code = ''.join(random.choices(characters, k=6))
        self.otp_created_at = timezone.now()
        self.save(update_fields=['otp_code', 'otp_created_at'])

    def is_otp_valid(self, entered_code):
        """Validates the entered OTP and checks expiration (10 minutes)."""
        if not self.otp_code or not self.otp_created_at:
            return False
        
        # Check if expired (10 minutes)
        if timezone.now() > self.otp_created_at + timedelta(minutes=10):
            return False
            
        return self.otp_code == entered_code.strip().upper()

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN or self.is_superuser

    def __str__(self):
        return self.email


class UserSubscription(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free Trial (30 Days)'),
        ('MONTHLY', 'Monthly Plan (10,000 TZS)'),
        ('ANNUAL', 'Annual Plan (100,000 TZS)'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired / Locked'),
        ('PENDING', 'Payment Pending'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.expiry_date:
            # Default free trial is 30 days
            self.expiry_date = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def check_expiration(self):
        """Checks if subscription has expired and locks access if necessary."""
        if self.expiry_date and timezone.now() > self.expiry_date and self.status != 'EXPIRED':
            self.status = 'EXPIRED'
            self.is_locked = True
            self.save()
        return self.is_locked

    def __str__(self):
        return f"{self.user.email} - {self.plan_type} ({self.status})"


class PaymentTransaction(models.Model):
    GATEWAY_CHOICES = [
        ('MOBILE_MONEY', 'Mobile Money (M-Pesa / Tigo Pesa / Airtel Money)'),
        ('BANK', 'Bank Transfer / Gateway'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    reference_code = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 10000.00 or 100000.00 TZS
    currency = models.CharField(max_length=10, default='TZS')
    gateway = models.CharField(max_length=30, choices=GATEWAY_CHOICES)
    plan_purchased = models.CharField(max_length=20)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status_text = 'Success' if self.is_successful else 'Pending'
        return f"Payment {self.reference_code} - {self.amount} TZS ({status_text})"