from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Customer

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = 'email',
