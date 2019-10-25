# -*- coding: utf-8 -*-
from tools import utils_random

from people.models.client import Client


def create_superuser(username='admin', password=None, email=None, first_name=None, last_name=None,
                     noinput=False):
    """
    Create a superuser Client.

    :param username:
    :type username: str
    :param password:
    :type password: str
    :param email:
    :type email: str
    :param first_name:
    :type first_name: str
    :param last_name:
    :type last_name: str
    :param noinput:
    :type noinput: bool
    :return: the created Client instance
    :rtype: Client
    """

    if password is None:
        password = utils_random.generate_password()

    _client = Client.objects.create_superuser(username=username, email=email, password=password,
                                              first_name=first_name, last_name=last_name)
    return _client
