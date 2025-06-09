from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager
from accounts.utils import user_photo_path


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("name"), max_length=150, blank=True)
    last_name = models.CharField(_("surname"), max_length=150, blank=True)

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    username = models.CharField(max_length=150, unique=True, blank=True)

    phone_number = PhoneNumberField(_("phone number"), null=True, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active." "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateTimeField(_("birth date"), blank=True, null=True)
    photo = models.ImageField(_("photo"), upload_to=user_photo_path, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.username:
            self.username = f"bd{self.pk}"
            super().save(update_fields=["username"])

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_registration_duration(self):
        return f"Time on site {timezone.now() - self.date_joined}"
