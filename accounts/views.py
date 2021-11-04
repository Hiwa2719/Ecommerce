from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

User = get_user_model()


class ProfileView(View):
    #  todo implement this view
    pass


class SignupView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('accounts:login')
    # def get_template_names(self):
