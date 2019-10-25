# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.db import models

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

    def save(self, *args, **kwargs):

        if self.id is not None:
            # prohibits the update
            raise utils_exception.ApplicationExc('`Client.save` forbidden. You should use only Client.update_profile.')

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
