# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import FrontRegistrationForm
from .serializers import ClientSerializer


class ClientView(APIView):

   def get(self, request):
      _serializer = ClientSerializer()

      return Response(_serializer.data)


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

      messages.error(request, 'An error occured while registration.')
      return redirect(reverse('join'))
   else:
      form = FrontRegistrationForm(executor=_executor)

      args = {'form': form}
      return render(request, 'people/join.html', args)
