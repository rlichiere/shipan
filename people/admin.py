# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models.address import Address
from .models.client import Client


class ClientAdmin(admin.ModelAdmin):
   list_display = ('username', 'first_name', 'last_name', 'date_joined', )
   list_filter = ('is_staff', 'is_superuser', 'is_active', )
   search_fields = ('username', 'first_name', 'last_name', )
   readonly_fields = ('last_login', 'date_joined', 'user_detail')
   fieldsets = (
      (None, {
         'fields': ('username', 'password', 'description', ())
      }),
      ('Personal info', {
         'fields': ('first_name', 'last_name', 'email', ),
      }),
      ('Permissions', {
         'fields': ('is_active', 'is_staff', 'is_superuser', ),
      }),
      ('Important dates', {
         'fields': ('last_login', 'date_joined', ),
      }),
      ('User info', {
         'fields': ('user_detail', ),
      }),
   )

   def get_readonly_fields(self, request, obj=None):
      _fields = list(self.readonly_fields)
      if obj is not None:
         _fields.append('password')
      return set(_fields)

   def user_detail(self, obj):
      if obj.id is not None:
         _url = reverse('admin:{}_{}_change'.format(User._meta.app_label, User._meta.model_name), args=[obj.id])
         return mark_safe('Change <a href="%s" target="_blank">%s</a> user information' % (_url, obj.get_full_name()))
      return mark_safe('This information will be available after the creation of the client')


class AddressAdmin(admin.ModelAdmin):
   list_display = ('is_default', )


admin.site.register(Client, ClientAdmin)
admin.site.register(Address, AddressAdmin)
