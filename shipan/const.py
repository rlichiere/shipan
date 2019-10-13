# -*- coding: utf-8 -*-


class _CLIENT_PASSWORD_CHANGE_METHOD(object):
   """
   Defines the methods available for changing the user password.
   """
   _EMAIL = 'EMAIL'
   _DIRECT = 'DIRECT'

   @property
   def EMAIL(self):
      """
      The `EMAIL` method sends a link to the user email, that allows the modification of its password for a limited amount of time.

      This method should be preferred for a Production environment.
      """
      return self._EMAIL

   @property
   def DIRECT(self):
      """
      The `DIRECT` method allows the modification of the password directly, without any email confirmation.

      This method should NOT be used on a Production environment.
      """
      return self._DIRECT

CLIENT_PASSWORD_CHANGE_METHOD = _CLIENT_PASSWORD_CHANGE_METHOD()
