# -*- coding: utf-8 -*-
from django.apps import apps
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

from tools import logger


class CustomUserModelBackend(ModelBackend):
    executor = None

    def authenticate(self, request, username=None, password=None, **kwargs):
        self.executor = request.user
        _l = logger.get('authenticate', username, self)
        try:
            _user = self.user_class.objects.get(username=username)
            if _user.check_password(password):
                _l.info('Authentication successful')
                return _user
        except self.user_class.DoesNotExist:
            _l.info('Authentication failed')
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        _l = logger.get('user_class', self.executor, self)

        if not hasattr(self, '_user_class'):
            _user_class = apps.get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            _l.debug('_user_class : %s' % _user_class)
            if not _user_class:
                raise ImproperlyConfigured('Could not get custom user model')
            return _user_class
