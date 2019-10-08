# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

from . import constants


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

   def __str__(self):
      return self.label

   def representation(self):
      return mark_safe('<img style="background-color:#%s; width: 16px; height: 16px">' % self.rgb)


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

   def __str__(self):
      return self.label

   def representation(self):
      return mark_safe('<img style="background-color:#%s; width: 16px; height: 16px">' % self.rgb)


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

   def __str__(self):
      return self.label

   # todo: default manager sort by position


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

   def __str__(self):
      return self.label


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

   category = models.ManyToManyField(help_text="""
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

   def __str__(self):
      return self.label


class ProductColouring(models.Model):

   product = models.ForeignKey(help_text="""
      Product of this colouring.
                               """,
                               to=ProductModel,
                               related_name='colouring')

   position = models.IntegerField(help_text="""
      Position of this product colouring in the product's colourings list.
                                  """)

   color = models.ForeignKey(help_text="""
      Color of this product colouring.
                             """,
                             to=ProductColor,
                             related_name='productscolourings')

   picture = models.CharField(help_text="""
      Picture filename of this product colouring.
                              """,
                              null=True,
                              max_length=200)
