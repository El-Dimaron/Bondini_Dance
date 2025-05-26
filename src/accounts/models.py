from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager


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
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateTimeField(_("birth date"), blank=True, null=True)
    photo = models.ImageField(_("photo"), upload_to="img/profiles", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

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


class Group(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)

    plan_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        choices=[
            ("group", "Абонемент"),
            ("personal", "Індивідуальне тренування"),
        ],
    )

    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    schedule_day = models.CharField(max_length=120, null=True, blank=True)
    schedule_time = models.TimeField(null=True, blank=True)
    trainer = models.CharField(max_length=100, null=True, blank=True)

    users = models.ManyToManyField(get_user_model(), related_name="dance_groups", blank=True)

    def __str__(self):
        return f"{self.name}"
