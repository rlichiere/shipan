# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .client import Client


class Address(models.Model):

   client = models.ForeignKey(to=Client,
                              related_name='addresses')

   is_default = models.BooleanField(help_text="""
       Indicates the default delivery address 
   """)

   class Meta:
      verbose_name_plural = 'Addresses'

   def save(self, *args, **kwargs):
      if self.is_default:
         try:
            _old = Address.objects.get(client=self.client, is_default=True)
         except Address.DoesNotExist:
            pass
         else:
            if self != _old:
               _old.is_default = False
               _old.save()
      super(Address, self).save(*args, **kwargs)
