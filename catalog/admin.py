# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe

from tools import admin_actions

from . import models


class ProductMainColorAdmin(admin.ModelAdmin):
   list_display = ('label', 'representation', 'rgb', 'name', 'detailed__colors', )
   readonly_fields = ('representation', 'detailed_colors', 'detailed__colors', )
   list_filter = ('colors', )

   @staticmethod
   def detailed_colors(instance):
      _html = '<ul>'
      for _color in instance.colors.all():
         _html += '<li>%s</li>' % _color.label
      _html += '</ul>'
      return mark_safe(_html)

   @staticmethod
   def detailed__colors(instance):
      _colors = instance.colors
      if _colors.count() == 1:
         _color = _colors.first()
         _html = '%s %s' % (_color.label, _color.representation())
      else:
         _html = ' '.join(['%s %s' % (_color.label, _color.representation()) for _color in _colors.all()])
      return mark_safe(_html)


class ProductColorAdmin(admin.ModelAdmin):
   list_display = ('label', 'representation', 'rgb', 'name', 'main__colors', )
   readonly_fields = ('representation', 'main__colors', )
   list_filter = ('main_colors', )

   @staticmethod
   def main__colors(instance):
      _colors = instance.main_colors
      if _colors.count() == 1:
         _color = _colors.first()
         _html = '%s %s' % (_color.label, _color.representation())
      else:
         _html = ' '.join(['%s %s' % (_color.label, _color.representation()) for _color in _colors.all()])
      return mark_safe(_html)


class ProductSizeAdmin(admin.ModelAdmin):
   list_display = ('label', 'name', 'position', )


class ProductCategoryAdmin(admin.ModelAdmin):
   list_display = ('label', 'name', )


class ProductModelAdmin(admin.ModelAdmin):
   list_display = ('label', 'name', )


class ProductColouringAdmin(admin.ModelAdmin):
   list_display = ('product', 'position', 'color', 'picture')


admin.site.register(models.ProductMainColor, ProductMainColorAdmin)
admin.site.register(models.ProductColor, ProductColorAdmin)
admin.site.register(models.ProductSize, ProductSizeAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductModel, ProductModelAdmin)
admin.site.register(models.ProductColouring, ProductColouringAdmin)

admin.site.add_action(admin_actions.backup_instances, 'Backup instances')
