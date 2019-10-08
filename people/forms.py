# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput

from .models.client import Client


class FrontAuthForm(AuthenticationForm):
   username = forms.CharField()
   password = forms.CharField(widget=PasswordInput())


class FrontRegistrationForm(UserCreationForm):

   email = forms.EmailField(required=True)

   class Meta:
      model = Client
      fields = (
         'username',
         'first_name',
         'last_name',
         'email',
         'password1',
         'password2',
      )

   def __init__(self, executor, *args, **kwargs):
      super(FrontRegistrationForm, self).__init__(*args, **kwargs)
      self.executor = executor

   def save(self, commit=True):
      user = super(FrontRegistrationForm, self).save(commit=False)
      user.first_name = self.cleaned_data['first_name']
      user.last_name = self.cleaned_data['last_name']
      user.email = self.cleaned_data['email']

      if commit:
         user.save()
         user.set_password(self.cleaned_data['password1'])
         user.save()

      return user
