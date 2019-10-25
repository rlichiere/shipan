# -*- coding: utf-8 -*-
"""
   Exceptions dedicated to this project.

   Any error should raise an exception inherited from the root class `Exc`:
      * `ConfigurationExc`
      * `LookupExc`
      * `ApplicationExc`

   Heritage:
   ```
   Exception
    +-- Exc
         +-- ConfigurationExc
         +-- LookupExc
         +-- ApplicationExc
   ```


"""

""" Exceptions """


class Exc(Exception):
    """
    Root of this project exceptions.

    This exception should never be raised directly, but rather be raised by a child implementation,
       such as ConfigurationExc, LookupExc, ApplicationExc, etc.
    """

    def __init__(self, *args, **kwargs):
        self._veil = ''
        if kwargs.has_key('veil'):
            self._veil = kwargs.pop('veil')

        super(Exc, self).__init__(*args)

    @property
    def veil(self):
        """
        Return the veiled (i.e reserved to staff members) information of the exception.

        Note: this information should be shown only to a superuser

        :return: the veiled information if raised, otherwise an empty str
        :rtype: str
        """
        return self._veil


class ConfigurationExc(Exc):
    """ Raised when a configuration is incoherent """
    pass


class LookupExc(Exc):
    """ The base class for the exceptions that are raised when a key or index used on a mapping or sequence is invalid """
    pass


class RuntimeExc(Exc):
    """ Raised when an error is detected that doesn't fall in any of the other categories """


class ApplicationExc(Exc):
    """
    Raised when the interpreter finds an internal error,
       but the situation does not look so serious to cause it to abandon all hope.

    You should report this to the author or maintainer of your Python interpreter.
    Be sure to report the version of the Python interpreter
       (sys.version; it is also printed at the start of an interactive Python session),
       the exact error message (the exception’s associated value)
       and if possible the source of the program that triggered the error.
    """


""" Tools """


def describe(exc):
    """
    Build the {module}.{class} description of the given exception.

    :param exc:
    :type exc: Exception
    :return: the given exception described by its module and class names
    :rtype: str
    """
    return '{module}.{exc_type}'.format(module=exc.__class__.__module__.split('.')[-1],
                                        exc_type=exc.__class__.__name__)


def labelize(exc):
    """
    Build a human readable label from the given exception.

    :param exc: the exception to convert as aa human readable label
    :type exc: Exception
    :return: the given exception converted as a human readable label
    :rtype: str
    """
    try:
        _excMessage = exc.message
    except AttributeError:
        _msgPart = ''
    else:
        _msgPart = ': {message}'.format(message=_excMessage)

    return '{description}{message_part}'.format(description=describe(exc),
                                                message_part=_msgPart)
