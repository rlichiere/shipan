# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe

from tools import admin_actions

from . import models


class ProductMainColorAdmin(admin.ModelAdmin):
    list_display = ('label_', 'name', 'representation', 'rgb', 'detailed__colors', )
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

    @staticmethod
    def label_(instance):
        return instance.getLabel()


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('label', 'representation', 'rgb', 'name', 'main__colors', )
    readonly_fields = ('representation', 'main__colors', )
    list_filter = ('main_colors', )

    @staticmethod
    def main__colors(instance):
        _mainColors = instance.main_colors
        if _mainColors.count() == 1:
            _mainColor = _mainColors.first()
            _html = '%s %s' % (_mainColor.getLabel(), _mainColor.representation())
        else:
            _html = ' '.join(['%s %s' % (_mainColor.getLabel(), _mainColor.representation()) for _mainColor in _mainColors.all()])
        return mark_safe(_html)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'position', )


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', )


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

    @staticmethod
    def color_(instance):
        return instance.color.representation()

    @staticmethod
    def main_colors(instance):
        return mark_safe(', '.join(_.representation() for _ in instance.color.main_colors.all()))


class ProductPictureAdmin(admin.ModelAdmin):
    list_display = ('product_', 'color_', 'picture', 'position', )
    list_filter = ('colouring__product__label', 'colouring__color__name', 'colouring__color__main_colors__name')
    readonly_fields = ('product_', 'color_')

    @staticmethod
    def product_(instance):
        return instance.colouring.product.label

    @staticmethod
    def color_(instance):
        return instance.colouring.color.label


class ProductSelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'label_', 'short_label_', 'start_at', 'ends_at', )

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
