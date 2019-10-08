# -*- coding: utf-8 -*-
from .models.client import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
   class Meta:
      model = Client
      fields = 'id', 'first_name'
