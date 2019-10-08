# -*- coding: utf-8 -*-


class _ProductAvailabilityClass(object):

   availabilities = {'hidden': 'Hidden', 'visible': 'Visible', 'orderable': 'Orderable'}

   @property
   def DEFAULT(self):
      return self.availabilities.keys()[0]

   @property
   def CHOICES(self):
      return [(_k, _v)  for _k, _v in self.availabilities.iteritems()]

PRODUCT_AVAILABILITY = _ProductAvailabilityClass()
