from django.contrib.auth.urls import *

from . import views as accounts_views

app_name = 'accounts'

urlpatterns = [
                  path('profile/', accounts_views.ProfileView.as_view(), name='profile'),
                  path('signup/', accounts_views.SignupView.as_view(), name='signup'),
              ] + urlpatterns
