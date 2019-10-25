# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext as _

from .models.client import Client


class FrontAuthForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput())


class FrontRegistrationForm(UserCreationForm):

    username = forms.EmailField(required=True)

    class Meta:
        model = Client
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def __init__(self, executor, *args, **kwargs):
        super(FrontRegistrationForm, self).__init__(*args, **kwargs)
        self.executor = executor

    def save(self, commit=True):
        user = super(FrontRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            user.set_password(self.cleaned_data['password1'])
            user.save()

        return user


class ChangeInformationForm(forms.Form):

    email = forms.EmailField(label=_('CLIENT_EMAIL'),
                             max_length=200,
                             required=False)
    first_name = forms.CharField(label=_('CLIENT_FIRST_NAME'),
                                 max_length=200,
                                 required=False)
    last_name = forms.CharField(label=_('CLIENT_LAST_NAME'),
                                max_length=200,
                                required=False)
    action = forms.CharField(initial='change_account_info',
                             widget=forms.HiddenInput())

    def __init__(self, executor, *args, **kwargs):
        self.executor = Client.objects.get(username=executor.username)
        super(ChangeInformationForm, self).__init__(*args, **kwargs)

        if self.executor.connects_with_email:
            self.fields['email'].required = True
        self.fields['email'].initial = self.executor.email

        self.fields['first_name'].initial = self.executor.first_name
        self.fields['last_name'].initial = self.executor.last_name


class SendLinkPasswordChangeForm(forms.Form):

    action = forms.CharField(initial='change_password_send_link',
                             widget=forms.HiddenInput(),
                             required=False)

    def __init__(self, executor, *args, **kwargs):
        super(SendLinkPasswordChangeForm, self).__init__(*args, **kwargs)
        self.executor = Client.objects.get(username=executor.username)


class ChangePasswordForm(forms.Form):

    new_password = forms.CharField(label=_('CLIENT_NEW_PASSWORD'),
                                   widget=forms.PasswordInput(),
                                   max_length=200)

    new_password_confirm = forms.CharField(label=_('CLIENT_NEW_PASSWORD_CONFIRMATION'),
                                           widget=forms.PasswordInput(),
                                           max_length=200)

    action = forms.CharField(initial='change_password',
                             widget=forms.HiddenInput())

    def clean(self):
        _cleanData = super(ChangePasswordForm, self).clean()

        if _cleanData['new_password'] == '' or _cleanData['new_password_confirm'] == '':
            raise forms.ValidationError(_('PASSWORD_SHOULD_NOT_BE_EMPTY'), code='invalid')

        if _cleanData['new_password'] != _cleanData['new_password_confirm']:
            raise forms.ValidationError(_('PASSWORDS_ARE_NOT_IDENTICAL'), code='invalid')

        return _cleanData
