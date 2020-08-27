from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rating, Comment

class BookForm(forms.Form):
    title = forms.CharField(max_length=200, label='Title')
    author = forms.CharField(max_length=200, label='Author')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['star', 'review']  

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
