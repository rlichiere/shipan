# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.db import models


class Client(User):

   description = models.TextField(help_text="""
      Description of the client. This information can be viewed only by a vendor.
                                  """,
                                  default='',
                                  blank=True)

   objects = UserManager()

   class Meta:
      verbose_name = 'Client'
