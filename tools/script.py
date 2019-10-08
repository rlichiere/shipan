# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from . import constants
from . import logger

from people.models.client import Client
from people.models.address import Address


u = User.objects.first()
l = logger.get(method_name='tools.script', executor=u)

try:
   cli = Client.objects.first()
except Client.DoesNotExist:
   pass

try:
   addr = Address.objects.first()
except Address.DoesNotExist:
   pass