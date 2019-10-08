# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from catalog.models import ProductModel


class ShopView(TemplateView):

   template_name = 'frontoffice/products.html'

   def get_context_data(self, **kwargs):
      context = super(ShopView, self).get_context_data(**kwargs)

      _filterCategories = self.request.GET.get('categories', '').split(',')
      _filterSizes = self.request.GET.get('sizes', '').split(',')
      _filterColors = self.request.GET.get('colors', '').split(',')

      _products = ProductModel.objects

      if _filterCategories[0] != '':
         _products = _products.filter(categories__name__in=_filterCategories)

      if _filterSizes[0] != '':
         _products = _products.filter(sizes__name__in=_filterSizes)

      if _filterColors[0] != '':
         _products = _products.filter(colourings__color__main_colors__name__in=_filterColors)

      context['products'] = _products.all()
      return context
