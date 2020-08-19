from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView

from .forms import UserRegisterForm
from django.urls import reverse_lazy

from django.utils.translation import ugettext as _


from django.views.generic import (
    CreateView,
    FormView,
    TemplateView)
# Create your views here.

class SignUpView(SuccessMessageMixin, CreateView):

    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = _("Now you are registered, try to log in!")


