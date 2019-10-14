# -*- coding: utf-8 -*-
import logging


__author__  = "Remi Lichiere <contact@reum.org>"
__status__  = "prototype"
__version__ = "0.0.1.0"
__date__    = "14 October 2019"


django_logger = logging.getLogger('shipan')


class _CommandExitCodeClass(object):

   @property
   def SUCCESS(self):
      return 0

   @property
   def ERROR(self):
      return 1

COMMAND_EXIT_CODE = _CommandExitCodeClass()


class LEVELS(object):

   _levels = {
      'DEBUG': django_logger.debug,
      'INFO': django_logger.info,
      'WARNING': django_logger.warning,
      'ERROR': django_logger.error,
      'EXCEPTION': django_logger.exception,
      'CRITICAL': django_logger.critical,
      'FATAL': django_logger.fatal,
   }
   DEBUG = 'DEBUG'
   INFO = 'INFO'
   WARNING = 'WARNING'
   ERROR = 'ERROR'
   EXCEPTION = 'EXCEPTION'
   CRITICAL = 'CRITICAL'
   FATAL = 'FATAL'

   @classmethod
   def getLevelMethod(cls, level):
      return cls._levels[level]


class ALPHABET(object):
   alpha10 = '0123456789'
   alpha26 = 'abcdefghijklmnopqrstuvwxyz'
   alpha36 = alpha10 + alpha26
   alpha62 = alpha36 + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   alpha79 = alpha62 + ',?;.:!%*$&#{([-|@)}'
   alpha86 = alpha79 + 'éèçàù'


CLIENT_DEFAULT_PWD_MIN_LEN = 8
CLIENT_DEFAULT_PWD_MAX_LEN = 16
