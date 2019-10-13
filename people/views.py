# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, HttpResponse, redirect, render, reverse
from django.views.generic import TemplateView

from shipan import config, const

from .forms import ChangePasswordForm, ChangeInformationForm, FrontRegistrationForm, SendLinkPasswordChangeForm
from .models.client import Client


def join(request):
   _executor = request.user
   if request.method == 'POST':
      form = FrontRegistrationForm(_executor, request.POST)
      if form.is_valid():
         form.save()
         messages.info(request, 'Thanks for joining. You are now logged in.')
         _executor = authenticate(request,
                                  username=form.cleaned_data['username'],
                                  password=form.cleaned_data['password1'])
         login(request, _executor)

         return HttpResponseRedirect(reverse('fo-home'))

      messages.error(request, 'An error occurred while registration.')

      return render(request, 'people/join.html', {'form': form})
   else:
      form = FrontRegistrationForm(executor=_executor)

      args = {'form': form}
      return render(request, 'people/join.html', args)


class ClientView(LoginRequiredMixin, TemplateView):
   template_name = 'people/client/account/account.html'
   template_name_change_password = 'people/client/account/account_change_password.html'

   def get_context_data(self, **kwargs):
      _executor = self.request.user
      context = super(ClientView, self).get_context_data(**kwargs)
      context['user'] = self.request.user
      context['config'] = config
      context['const'] = const

      _action = self.request.GET.get('action')

      try:
         if _action == 'change_password':
            change_password_form = ChangePasswordForm()
            context['change_password_form'] = change_password_form
            self.template_name = 'people/client/account/account_change_password.html'

         else:
            change_info_form = ChangeInformationForm(executor=_executor)
            context['change_info_form'] = change_info_form

            change_password_send_link_form = SendLinkPasswordChangeForm(executor=_executor)
            context['change_password_send_link_form'] = change_password_send_link_form

      except StandardError as e:
         context['error'] = {
            'label': e.__class__.__name__,
            'detail': e.message,
         }

      return context

   def post(self, *args, **kwargs):
      _executor = Client.objects.get(username=self.request.user.username)
      _action = self.request.POST.get('action')

      if _action == 'change_account_info':
         _form = ChangeInformationForm(_executor, self.request.POST)
         if not _form.is_valid():
            messages.error(self.request, 'Error while changing profile information' % _form.errors)
            return HttpResponse(render(self.request, template_name=self.template_name_change_password))
         _executor.email = _form.cleaned_data['email']
         _executor.username = _form.cleaned_data['email']
         _executor.first_name = _form.cleaned_data['first_name']
         _executor.last_name = _form.cleaned_data['last_name']
         _executor.save()
         messages.info(self.request, 'Account information saved')

      elif _action == 'change_password_send_link':
         messages.warning(self.request, 'Send change password link is not yet implemented. Please use CLIENT_PASSWORD_CHANGE_METHOD.DIRECT')
         # messages.info(self.request, 'Change password link sent')

      elif _action == 'change_password':

         _form = ChangePasswordForm(self.request.POST)
         if not _form.is_valid():
            messages.error(self.request, 'Error while changing password (error: %s)' % _form.errors)
            return HttpResponse(render(self.request, template_name=self.template_name_change_password))

         else:
            _executor.set_password(_form.cleaned_data['new_password'])
            _executor.save()
            _executor = authenticate(self.request,
                                     username=_executor.username,
                                     password=_form.cleaned_data['new_password'])
            login(self.request, _executor)

            messages.info(self.request, 'Password changed')

      else:
         messages.error(self.request, 'Unknown action : %s' % _action)

      return redirect(reverse('client-account'))
