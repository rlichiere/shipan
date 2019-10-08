# -*- coding: utf-8 -*-
from . import settings

from tools import utils_version

BACKUP_ROOT = '%s/_backup' % settings.BASE_DIR

VERSION = utils_version.Version(
   major=0,
   minor=1,
   build=1,
   level=utils_version.VersionLevel.BETA,
   revision=1,
   comment=''
)
