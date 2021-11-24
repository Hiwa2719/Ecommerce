from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, View, UpdateView

from ecommerce.utils import EmailVerificationTokenGenerator
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


class EmailVerification(TemplateView):
    template_name = 'accounts/email_verification_send.html'

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
                'token': EmailVerificationTokenGenerator().make_token(customer),
                'protocol': 'http'
            }
            body = loader.render_to_string('accounts/verification_email_template.html', context)
            send_mail(
                subject=f'Email verification at {current_site.name}',
                message=body,
                from_email='hiahmadyan@gmail.com',
                recipient_list=[customer.email, ]
            )
            return super().get(request, *args, **kwargs)
        raise Http404


class EmailVerificationLinkCheckView(View):
    def dispatch(self, *args, **kwargs):
        self.customer = self.get_user(kwargs.get('uidb64'))
        if self.customer is not None:
            token = kwargs.get('token')
            if token:
                if EmailVerificationTokenGenerator().check_token(self.customer, token):
                    self.customer.verify()
                    return redirect('accounts:verification_success')
        raise Http404

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            customer = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist, ValidationError):
            customer = None
        return customer


class EmailVerificationSuccess(TemplateView):
    template_name = 'accounts/verification_successful.html'


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


class PersonalInfoUpdateView(UpdateView):
    model = Customer
    fields = 'username',
    success_url = reverse_lazy('accounts:profile')
