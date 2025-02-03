from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom User model with extended fields for registration."""
    full_name = models.CharField(_("Full Name"), max_length=255)
    username = models.CharField(
        _("Username"), max_length=150, unique=True,
        error_messages={"unique": _("A user with that username already exists.")},
    )
    password = models.CharField(_("Password"), max_length=128)

    # Disable unused fields from AbstractUser
    first_name = None
    last_name = None

    def __str__(self):
        return self.username
