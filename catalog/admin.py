# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import QuerySet

from tools import admin_actions

from . import models



class ColorFormatter(object):

    @staticmethod
    def render(colors):
        """
        Render given colors as HTML.

        :param colors: color (or list of colors) to render
        :type colors: list, Color
        :return: list of colors formatted as safe HTML
        """
        if type(colors) is QuerySet:
            _html = ', '.join(['%s %s' % (_color.representation(), _color.getLabel()) for _color in colors.all()])
        else:
            _html = '%s %s' % (colors.representation(), colors.getLabel())
        return mark_safe(_html)


class ProductMainColorAdmin(admin.ModelAdmin):
    list_display = ('label_', 'name', 'representation', 'rgb', 'detailed_colors', )
    readonly_fields = ('representation', 'detailed_colors', )
    list_filter = ('colors', )
    search_fields = ('loc_label', 'name', 'rgb', 'colors__loc_label', )

    @staticmethod
    def detailed_colors(instance):
        return ColorFormatter.render(instance.colors.all())

    @staticmethod
    def label_(instance):
        return instance.getLabel()


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('getLabel', 'representation', 'rgb', 'name', 'main__colors', )
    readonly_fields = ('representation', 'main__colors', )
    list_filter = ('main_colors', )
    search_fields = ('loc_label', 'name', 'rgb', )

    @staticmethod
    def main__colors(instance):
        return ColorFormatter.render(instance.main_colors.all())


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'position', )
    search_fields = ('label', 'name', )


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', )
    search_fields = ('label', 'name', )


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'categories_', 'main_category', )
    list_filter = ('categories', )
    search_fields = ('label', 'name', 'loc_description', )

    @staticmethod
    def categories_(instance):
        return ', '.join(_.label for _ in instance.categories.all())


class ProductColouringAdmin(admin.ModelAdmin):
    list_display = ('product', 'position', 'color_', 'main_colors', )
    list_filter = ('product', 'color', )
    readonly_fields = ('color_', 'main_colors', )
    search_fields = ('product__label', 'product__name', 'color__loc_label', 'color__main_colors__loc_label', )

    @staticmethod
    def color_(instance):
        return ColorFormatter.render(instance.color)

    @staticmethod
    def main_colors(instance):
        return ColorFormatter.render(instance.color.main_colors.all())


class ProductPictureAdmin(admin.ModelAdmin):
    list_display = ('product_', 'color_', 'picture', 'position', )
    list_filter = ('colouring__product__label', 'colouring__color__name', 'colouring__color__main_colors__name', )
    readonly_fields = ('product_', 'color_', )
    search_fields = ('colouring__product__label', 'colouring__product__name', 'colouring__color__loc_label', 'picture', )

    @staticmethod
    def product_(instance):
        return instance.colouring.product.label

    @staticmethod
    def color_(instance):
        return ColorFormatter.render(instance.colouring.color)


class ProductSelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'label_', 'short_label_', 'start_at', 'ends_at', )
    search_fields = ('name', 'kind', 'loc_label', )

    @staticmethod
    def label_(instance):
        return instance.getLabel()

    @staticmethod
    def short_label_(instance):
        return instance.getShortLabel()


admin.site.register(models.ProductMainColor, ProductMainColorAdmin)
admin.site.register(models.ProductColor, ProductColorAdmin)
admin.site.register(models.ProductSize, ProductSizeAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductModel, ProductModelAdmin)
admin.site.register(models.ProductColouring, ProductColouringAdmin)
admin.site.register(models.ProductPicture, ProductPictureAdmin)
admin.site.register(models.ProductSelection, ProductSelectionAdmin)

admin.site.add_action(admin_actions.backup_instances, 'Backup instances')