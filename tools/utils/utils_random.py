# -*- coding: utf-8 -*-
import random

from .. import constants as const


def generate_password(length=const.CLIENT_DEFAULT_PWD_MIN_LEN, max_length=const.CLIENT_DEFAULT_PWD_MIN_LEN):
   return ''.join(random.choice(const.ALPHABET.alpha79) for _ in range(random.randint(length, max_length)))
