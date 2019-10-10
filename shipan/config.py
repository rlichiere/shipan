# -*- coding: utf-8 -*-
from . import settings

from tools import utils_version

BACKUP_ROOT = '%s/_backup' % settings.BASE_DIR

VERSION = utils_version.Version(
   project_name='ShipanShop',
   major=0,
   minor=1,
   build=1,
   level=utils_version.VersionLevel.BETA,
   revision=1,
   comment='',
   publish_year=2019,
   publish_month=10,
   publish_day=10,
   author_name='Remi LICHIERE',
   author_email='contact@reum.org',
)
