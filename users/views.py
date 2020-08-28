from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView

from django.urls import reverse_lazy

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm)

from django.views.generic import (
    CreateView,
    FormView,
    TemplateView)
from review.models import  Follow

from django.http import HttpResponseRedirect
# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):

    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = _("Now you are registered, try to log in!")

class UserDetailView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'users/user_detail.html'

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = UserUpdateForm
    p_form = ProfileUpdateForm()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now your profile is updated!"

    def form_valid(self, form):
        self.request.user.username = self.request.POST['username']
        self.request.user.email = self.request.POST['email']
        self.request.user.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        return initial


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = ProfileUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now you photo is updated"

    def form_valid(self, form):
        if 'image' in self.request.FILES:
            self.request.user.profile.image = self.request.FILES['image']
            self.request.user.profile.save()
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                                 'Your profile pic is not change')
            return HttpResponseRedirect(reverse_lazy('UserProfile'))

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['image'] = self.request.user.profile.image
        return initial

@login_required
def follow(request, pk):
    if request.method == 'GET':
        user = request.user
        to_user = get_object_or_404(User, pk=pk)
        is_followed = 1
        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            if followed:
                followed.delete()
                is_followed=0
        except :
            follow = Follow(follower = user, following = to_user)
            follow.save()
            is_followed =1
        num_following = Follow.objects.filter(follower=to_user).count()
        num_follower = Follow.objects.filter(following=to_user).count()
        print(num_follower, num_following)
        context = {
            'user': user,
            'to_user': to_user, 
            'following': num_following, 
            'follower': num_follower,
            'is_followed': is_followed,
            }
        return render(request, 'users/user_profile.html', context=context)
    else:
        url = request.META.get('HTTP_REFERER')
        return  HttpResponseRedirect(url)

