from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, View

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


class EmailVerification(View):
    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        if not customer.verified_email:
            current_site = get_current_site(request)
            context = {
                'email': customer.email,
                'domain': current_site.domain,
                'site_name': current_site.name,
                'uid': urlsafe_base64_encode(force_bytes(customer.id)),
                'user': customer,
                'token': default_token_generator.make_token(customer),
                'protocol': 'http'
            }
            body = loader.render_to_string('accounts/verification_email_template.html', context)
            send_mail(
                subject=f'Email verification at {current_site.name}',
                message=body,
                from_email='hiahmadyan@gmail.com',
                recipient_list=[customer.email, ]
            )
        raise Http404


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
