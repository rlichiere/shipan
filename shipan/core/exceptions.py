# -*- coding: utf-8 -*-


class ShipanError(Exception):

    def __init__(self, message, veil=None, executor=None, **kwargs):
        self._executor = executor if executor else None
        self._veil = veil if veil else None

        super(ShipanError, self).__init__(message, **kwargs)

    @property
    def veil(self):
        """
        Return the veiled (i.e reserved to staff members) information of the error.

        Note: this information should be shown only to a superuser

        :return: the veiled information if given, otherwise an empty str
        :rtype: str
        """
        return self._veil

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.message)


class ShipanSecurityError(ShipanError):
    pass
