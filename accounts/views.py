from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView

from .forms import SignupForm
from .models import Customer

User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    #  todo implement this view
    pass


class SignupView(CreateView):
    form_class = SignupForm
    model = Customer
    success_url = reverse_lazy('accounts:login')


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('accounts:delete_success')

    def get_object(self, queryset=None):
        return self.request.user.customer


class DeleteSuccessView(TemplateView):
    template_name = 'accounts/delete_success.html'


class OrderListView(ListView):
    # todo implement this view with Order model
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
