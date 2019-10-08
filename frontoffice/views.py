# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse

from catalog.models import ProductModel


class ShopView(TemplateView):

   template_name = 'frontoffice/products.html'

   def get_context_data(self, **kwargs):
      context = super(ShopView, self).get_context_data(**kwargs)

      _filterSelection = self.request.GET.get('selection')
      _filterCategories = self.request.GET.get('categories', '').split(',')
      _filterSizes = self.request.GET.get('sizes', '').split(',')
      _filterColors = self.request.GET.get('colors', '').split(',')

      _products = ProductModel.objects

      if _filterSelection:
         _products = _products.filter(selections__name=_filterSelection)

      if _filterCategories[0] != '':
         _products = _products.filter(categories__name__in=_filterCategories)

      if _filterSizes[0] != '':
         _products = _products.filter(sizes__name__in=_filterSizes)

      if _filterColors[0] != '':
         _products = _products.filter(colourings__color__main_colors__name__in=_filterColors)

      context['products'] = _products.all().distinct()
      return context


class ProductView(TemplateView):

   template_name = 'frontoffice/product.html'

   def __init__(self, *args, **kwargs):
      super(ProductView, self).__init__(*args, **kwargs)
      self.product = None

   def get(self, *args, **kwargs):
      _filterProduct = self.request.GET.get('model')

      try:
         self.product = ProductModel.objects.get(name=_filterProduct)
      except ProductModel.DoesNotExist:
         messages.error(self.request, 'Unknown product')
         return redirect(reverse('fo-home'))
      return super(ProductView, self).get(*args, **kwargs)

   def get_context_data(self, **kwargs):
      context = super(ProductView, self).get_context_data(**kwargs)

      _color = self.request.GET.get('color')
      context['color'] = _color

      context['product'] = self.product
      return context
