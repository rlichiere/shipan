# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import DynamicPage


class DynamicPageAdmin(admin.ModelAdmin):
   list_display = ('name', 'title_', 'flow', 'flow_position', )
   list_filter = ('flow', )
   readonly_fields = ('title_', )

   @staticmethod
   def title_(instance):
      return instance.getTitle()


admin.site.register(DynamicPage, DynamicPageAdmin)
