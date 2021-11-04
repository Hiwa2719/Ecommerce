from django.views.generic import CreateView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render


class ProfileView(View):
    #  todo implement this view
    pass


class SignupView(CreateView):
    form = UserCreationForm
    success_url = reverse_lazy('accounts:login')
