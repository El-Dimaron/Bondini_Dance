from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (CreateView, RedirectView, TemplateView,
                                  UpdateView)

from accounts.forms import UserRegistrationForm, UserUpdateForm
from accounts.models import User
from accounts.services.emails import send_registration_email
from accounts.utils import TokenGenerator


class UserLoginView(LoginView): ...  # NOQA:E701


class UserLogoutView(LogoutView): ...  # NOQA:E701


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "edit_profile.html"
    form_class = UserUpdateForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("accounts:user_profile")

    def get_object(self):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        if not self.request.user.phone_number:
            initial["phone_number"] = "+380"
        return initial


class UserRegistrationView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object: get_user_model() = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        send_registration_email(user_instance=self.object, request=self.request)

        messages.success(self.request, "Підтвердження реєстрації надіслано")
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial["phone_number"] = "+380"
        return initial


class UserActivationView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, uid, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uid))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return HttpResponse("Invalid data")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)
            messages.success(self.request, "Вітаємо на сайті!")
            return super().get(request, *args, **kwargs)

        return HttpResponse("Invalid data")


# class UserRegistrationView(CreateView):
#     template_name = "registration/registration_form.html"
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy("index")
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         user = form.save()
#
#         login(self.request, user)
#
#         return response


def users(request: HttpRequest) -> HttpResponse:
    word = ""
    try:
        count = int(request.GET.get("count", 1))
    except ValueError:
        count = 1
    if count > 1:
        word = "s"
    User.generate_users(count)
    return HttpResponse(f"Generated {count} user{word}")
