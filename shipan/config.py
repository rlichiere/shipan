# -*- coding: utf-8 -*-
from . import settings
from . import const

from tools import utils_version


BACKUP_ROOT = '%s/%s' % (settings.BASE_DIR, settings.SHIPAN['DATA']['ROOT']['FOLDER'])

VERSION = utils_version.Version(
    project_name='ShipanShop',
    major=0,
    minor=0,
    build=1,
    level=utils_version.VersionLevel.BETA,
    revision=1,
    comment='',
    publish_year=2019,
    publish_month=10,
    publish_day=26,
    author_name='Remi LICHIERE',
    author_email='contact@reum.org',
)

# Overloadable properties
CLIENT_PASSWORD_CHANGE_METHOD = const.CLIENT_PASSWORD_CHANGE_METHOD.DIRECT

RUNNING_ON_WINDOWS = False

try:
    from .config_custom import *
except ImportError:
    pass
