from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Ensure unique email addresses for secure signups
    email = models.EmailField(_('email address'), unique=True)
    
    class RoleChoices(models.TextChoices):
        USER = 'USER', _('Normal User')
        ADMIN = 'ADMIN', _('Admin')

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        help_text=_("Designates the user's primary access level.")
    )
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.ADMIN or self.is_superuser