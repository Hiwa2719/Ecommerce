from django.contrib.auth.urls import *
from django.urls import reverse_lazy

from . import views as accounts_views

app_name = 'accounts'

urlpatterns = [
                  path('email_verification/', accounts_views.EmailVerification.as_view(), name='email_verification'),
                  path('verify_email/<uidb64>/<token>/', accounts_views.EmailVerificationLinkCheckView.as_view(),
                       name='link_verification'),
                  path('verification-successful/', accounts_views.EmailVerificationSuccess.as_view(),
                       name='verification_success'),
                  path('profile/', accounts_views.ProfileView.as_view(), name='profile'),
                  path('signup/', accounts_views.SignupView.as_view(), name='signup'),
                  path('delete-account/', accounts_views.DeleteAccountView.as_view(), name='delete_account'),
                  path('delete-success/', accounts_views.DeleteSuccessView.as_view(), name='delete_success'),
                  path('ordre-list/', accounts_views.OrderListView.as_view(), name='order-list'),
                  path('password_change/',
                       views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')),
                       name='password_change'),
                  path('password_reset/',
                       views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
                       name='password_reset'),
                  path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
                      success_url=reverse_lazy('accounts:password_reset_complete')),
                       name='password_reset_confirm'),
              ] + urlpatterns
