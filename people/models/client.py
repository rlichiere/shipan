# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, UserManager
from django.db import models


class Client(User):

   description = models.TextField(default='',
                                  blank=True,
                                  help_text="""
      Description of the client. This information can be viewed only by a vendor.
                                  """)

   objects = UserManager()

   class Meta:
      verbose_name = 'Client'

   def save(self, **kwargs):
      _creation = False
      if self.id is None:
         _creation = True

      super(Client, self).save(**kwargs)

      if _creation:
         self.set_password(self.password)
         self.save()
