# -*- coding: utf-8 -*-
import logging


__author__  = "Remi Lichiere <contact@reum.org>"
__status__  = "prototype"
__version__ = "0.0.1.0"
__date__    = "03 October 2019"


django_logger = logging.getLogger('shipan')


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
