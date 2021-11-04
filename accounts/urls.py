from django.contrib.auth.urls import *
from django.urls import reverse_lazy

from . import views as accounts_views

app_name = 'accounts'

urlpatterns = [
                  path('profile/', accounts_views.ProfileView.as_view(), name='profile'),
                  path('signup/', accounts_views.SignupView.as_view(), name='signup'),
                  path('password_change/',
                       views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done'))),
                  path('password_reset/',
                       views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')))
              ] + urlpatterns
