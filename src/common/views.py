from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.forms import UserRegistrationForm


class IndexView(TemplateView):
    template_name = "index.html"


class UserLoginView(LoginView): ...  # NOQA:E701


class UserLogoutView(LogoutView): ...  # NOQA:E701


class UserRegistrationView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        login(self.request, user)

        return response
