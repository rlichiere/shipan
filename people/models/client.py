# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.db import models

from tools import logger
from tools import utils_exception


class Client(User):
    description = models.TextField(help_text="""
        Description of the client. This information can be viewed only by a vendor.
                                   """,
                                   default='',
                                   blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Client'
        ordering = ('first_name', 'last_name')

    def save(self, *args, **kwargs):
        _l = logger.get('save', obj=self)

        if self.id is not None:

            # the update of email, first_name or last_name fields must be done via Client.update_profile()
            _updateFields = kwargs.get('update_fields', None)
            if _updateFields is not None:

                if len(set(_updateFields) & {'email', 'first_name', 'last_name'}) > 0:
                    # forbidden field found in kwargs
                    _l.error('A forbidden call to Client.save() occurred.')
                    _reason = 'The update of email, first_name or last_name fields must be done via Client.update_profile().'
                    _l.error('- Reason: %s' % _reason)
                    _l.error('- args  : %s' % str(args))
                    _l.error('- kwargs: %s' % kwargs)
                    raise utils_exception.ApplicationExc('`Client.save()` error. Reason: %s' % _reason)
                _l.info('Client update allowed for field(s): %s' % ', '.join(_updateFields))

        super(Client, self).save(*args, **kwargs)

    def update_profile(self, email=None, first_name=None, last_name=None):
        if email:
            self.email = email

            if self.connects_with_email:
                self.username = email

        if first_name:
            self.first_name = first_name

        if last_name:
            self.last_name = last_name

        super(Client, self).save()

    @property
    def connects_with_email(self):
        return self.username == self.email