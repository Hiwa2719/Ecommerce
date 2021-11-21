from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import SignupForm

User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    #  todo implement this view
    pass


class SignupView(CreateView):
    form_class = SignupForm
    model = User
    success_url = reverse_lazy('accounts:login')
