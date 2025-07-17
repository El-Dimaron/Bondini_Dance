from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.utils import TokenGenerator


def send_registration_email(user_instance: get_user_model(), request: HttpRequest) -> None:
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user_instance.id))
    token = TokenGenerator().make_token(user_instance)
    activation_link = request.build_absolute_uri(reverse("accounts:activate_user", kwargs={"uid": uid, "token": token}))

    print("Sending from:", settings.EMAIL_HOST_USER)
    print("To:", user_instance.email)
    print("Using password?", bool(settings.EMAIL_HOST_PASSWORD))
    print("Using app password?", "<yes if you know>")

    message = render_to_string(
        template_name="emails/registration_email.html",
        context={
            "user": user_instance,
            "domain": domain,
            "token": token,
            "uid": uid,
            "activation_link": activation_link,
            "year": timezone.now().year,
        },
    )

    email = EmailMessage(
        subject="Registration email from Bondini Dance",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_instance.email],
        bcc=[settings.EMAIL_HOST_USER],
    )

    email.content_subtype = "html"
    email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
