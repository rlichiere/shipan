# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class DynamicPage(models.Model):

   name = models.CharField(help_text="""
      Intern name of the page.
                           """,
                           max_length=200)

   title = models.CharField(help_text="""
      Title of the page.
                            """,
                            max_length=200)

   content = models.TextField(help_text="""
      Content of the page.
                              """,
                              default='',
                              blank=True)

   flow = models.CharField(help_text="""
      Flow in the page.
                           """,
                           choices=[('footer', 'Footer')],
                           max_length=200)

   flow_position = models.IntegerField(help_text="""
      Position in flow.
                                       """,
                                       default=1)

   class Meta:
      ordering = ['flow_position']

   def __str__(self):
      return self.title
