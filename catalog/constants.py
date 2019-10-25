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


class _ProductSelectionKind(object):

   kinds = ['NEW', 'SEASON', ]

   @property
   def NEW(self):
      return self.kinds[0]

   @property
   def SEASON(self):
      return self.kinds[1]

   @property
   def CHOICES(self):
      return [(_k, _k) for _k in self.kinds]

PRODUCT_SELECTION_KIND = _ProductSelectionKind()
