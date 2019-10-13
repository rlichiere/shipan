# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import DynamicPage


class DynamicPageAdmin(admin.ModelAdmin):
   list_display = ('name', 'title', 'flow', 'flow_position', )
   list_filter = ('flow', )


admin.site.register(DynamicPage, DynamicPageAdmin)
