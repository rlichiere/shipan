# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe

from . import constants
from tools.utils import utils_price


@python_2_unicode_compatible
class ProductMainColor(models.Model):

   name = models.CharField(help_text="""
      Intern name of the color.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the color.
                            """,
                            unique=True,
                            max_length=200)

   rgb = models.CharField(help_text="""
      RGB code of the color, as hexadecimal.
                          """,
                          max_length=6)

   class Meta:
      ordering = ['name']

   def __str__(self):
      return self.label

   def representation(self):
      return mark_safe('<img style="background-color:#%s; width: 16px; height: 16px">' % self.rgb)

   @property
   def rgb_s(self):
      return '#%s' % self.rgb


@python_2_unicode_compatible
class ProductColor(models.Model):

   name = models.CharField(help_text="""
      Intern name of the color.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the color.
                            """,
                            unique=True,
                            max_length=200)

   rgb = models.CharField(help_text="""
      RGB code of the color, as hexadecimal.
                          """,
                          max_length=6)

   main_colors = models.ManyToManyField(help_text="""
      Main colors that represent this color.
                                        """,
                                        to=ProductMainColor,
                                        related_name='colors')

   class Meta:
      ordering = ['name']

   def __str__(self):
      return self.label

   def representation(self):
      return mark_safe('<img style="background-color:#%s; width: 16px; height: 16px">' % self.rgb)

   @property
   def rgb_s(self):
      return '#%s' % self.rgb


@python_2_unicode_compatible
class ProductSize(models.Model):

   name = models.CharField(help_text="""
      Intern name of the size.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the size.
                            """,
                            unique=True,
                            max_length=200)

   position = models.IntegerField(help_text="""
      Position of this size in the sizes's list.
                                  """,
                                  unique=True,
                                  default=1)

   class Meta:
      ordering = ['position']

   def __str__(self):
      return self.label


@python_2_unicode_compatible
class ProductCategory(models.Model):

   name = models.CharField(help_text="""
      Intern name of the category.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the category.
                            """,
                            unique=True,
                            max_length=200)

   class Meta:
      verbose_name_plural = 'Product categories'
      ordering = ['name']

   def __str__(self):
      return self.label


@python_2_unicode_compatible
class ProductModel(models.Model):

   name = models.CharField(help_text="""
      Intern name of the model.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the model.
                            """,
                            unique=True,
                            max_length=200)

   description = models.TextField(help_text="""
      Description of the model, shown in product detail.
                            """,
                                  default='',
                                  blank=True)

   categories = models.ManyToManyField(help_text="""
      Categories of this model.
                                       """,
                                       to=ProductCategory,
                                       related_name='productmodels')

   main_category = models.ForeignKey(help_text="""
      Main category of the model.
                                     """,
                                     to=ProductCategory,
                                     related_name='mainproductsmodels')

   sizes = models.ManyToManyField(help_text="""
      Sizes available for this model.
                                  """,
                                  to=ProductSize,
                                  related_name='productmodels')

   price = models.FloatField(help_text="""
      Price of the product model.
                             """,
                             null=False)

   visibility = models.CharField(help_text="""
      Indicates the availability of the model.
                                 """,
                                 choices=constants.PRODUCT_AVAILABILITY.CHOICES,
                                 default=constants.PRODUCT_AVAILABILITY.DEFAULT,
                                 max_length=200)

   def price_justified(self):
      """
      Return the ProductModel price, as str, with zero justified cents.

      :return: the price of the instance, of which the cents are justified with zeros
      :rtype: str
      """
      return utils_price.justified(self.price)

   def __str__(self):
      return self.label

   class Meta:
      ordering = ['name']

   @property
   def getColouringsColorNames(self):
      return self.colourings.all().values_list('color__name', flat=True)


@python_2_unicode_compatible
class ProductColouring(models.Model):

   product = models.ForeignKey(help_text="""
      Product of this colouring.
                               """,
                               to=ProductModel,
                               related_name='colourings')

   position = models.IntegerField(help_text="""
      Position of this product colouring in the product's colourings list.
                                  """)

   color = models.ForeignKey(help_text="""
      Color of this product colouring.
                             """,
                             to=ProductColor,
                             related_name='productscolourings')

   class Meta:
      ordering = ['product__name', 'position']

   def __str__(self):
      return self.product.label + ' #' + self.color.label


class ProductPicture(models.Model):
   colouring = models.ForeignKey(help_text="""
      ProductColouring of this picture.
                               """,
                               to=ProductColouring,
                               related_name='pictures')

   picture = models.CharField(help_text="""
      Picture filename of this product colouring.
                              """,
                              blank=True,
                              null=True,
                              max_length=200)

   position = models.IntegerField(help_text="""
      Position of this product colouring in the product's colourings list.
                                  """,
                                  default=1)

   class Meta:
      ordering = ['colouring__product__name', 'position']


@python_2_unicode_compatible
class ProductSelection(models.Model):

   name = models.CharField(help_text="""
      Intern name of the selection.
                           """,
                           unique=True,
                           max_length=200)

   label = models.CharField(help_text="""
      Label of the selection.
                            """,
                            unique=True,
                            max_length=200)

   products = models.ManyToManyField(help_text="""
      Products of this selection.
                                     """,
                                     to=ProductModel,
                                     related_name='selections')

   def __str__(self):
      return self.label

   class Meta:
      ordering = ['name']
