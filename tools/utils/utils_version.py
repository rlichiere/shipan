# -*- coding: utf-8 -*-
from . import utils_exception as exc


class _VersionLevel(object):

    def __init__(self):
        self._alpha = 'Alpha'
        self._beta = 'Beta'
        self._rc = 'ReleaseCandidate'
        self._release = 'Release'

        self._levelCodes = {
            self._alpha: 'alpha',
            self._beta: 'beta',
            self._rc: 'rc',
            self._release: 'release',
        }

    @property
    def ALPHA(self):
        return self._alpha

    @property
    def BETA(self):
        return self._beta

    @property
    def RELEASE_CANDIDATE(self):
        return self._rc

    @property
    def RELEASE(self):
        return self._release

    def getLevelCode(self, level):
        try:
            return self._levelCodes[level]
        except KeyError:
            raise exc.LookupExc('Unexpected level: %s' % level)


VersionLevel = _VersionLevel()


class Version(object):

    def __init__(self, project_name,
                 major, minor, build, level, revision,
                 publish_year, publish_month, publish_day,
                 publish_hour='', publish_minute='', publish_second='',
                 comment='',
                 author_name='', author_email='',
                 maintainer_name='', maintainer_email=''):
        self._projectName = str(project_name)

        self._major = str(major)
        self._minor = str(minor)
        self._build = str(build)
        self._level = str(level)
        self._revision = str(revision)

        self._comment = str(comment)

        self._authorName = author_name
        self._authorEmail = author_email
        self._maintainerName = maintainer_name
        self._maintainerEmail = maintainer_email

        self._publishYear = str(publish_year)
        self._publishMonth = str(publish_month).rjust(2, '0')
        self._publishDay = str(publish_day).rjust(2, '0')
        self._publishHour = str(publish_hour).rjust(2, '0')
        self._publishMinute = str(publish_minute).rjust(2, '0')
        self._publishSecond = str(publish_second).rjust(2, '0')

    """ Project informmation """

    @property
    def Project(self):
        return self._projectName

    """ Version information """

    @property
    def Version(self):
        return '.'.join([self._major, self._minor, self._build])

    @property
    def Revision(self):
        return ' '.join([self._level, self._revision])

    @property
    def revision(self):
        return '-rev'.join([VersionLevel.getLevelCode(self._level), self._revision])

    @property
    def VersionFull(self):
        return ' '.join([self.Version, self.Revision])

    @property
    def versionFull(self):
        return '.'.join([self.Version, self.revision])

    @property
    def VersionCode(self):
        return '.'.join([self.versionFull, self.publishDate])

    @property
    def VersionCodeFull(self):
        return '.'.join([self.versionFull, self.publishDateTime])

    """ Publish date """

    @property
    def PublishYear(self):
        return self._publishYear

    @property
    def PublishMonth(self):
        return self._publishMonth

    @property
    def PublishDay(self):
        return self._publishDay

    @property
    def PublishHour(self):
        return self._publishHour

    @property
    def PublishMinute(self):
        return self._publishMinute

    @property
    def PublishSecond(self):
        return self._publishSecond

    @property
    def PublishDate(self):
        return '/'.join([self._publishYear, self._publishMonth, self._publishDay])

    @property
    def publishDate(self):
        return '-'.join([self._publishYear, self._publishMonth, self._publishDay])

    @property
    def PublishTime(self):
        return '%sh%sm%ss' % (self._publishHour, self._publishMinute, self._publishSecond)

    @property
    def PublishDateTime(self):
        return ' '.join([self.PublishDate, self.PublishTime])

    @property
    def publishDateTime(self):
        return '.'.join([self.publishDate, self.PublishTime])

    """ Author information """

    @property
    def Author(self):
        return self._authorName

    @property
    def AuthorContact(self):
        return self._authorEmail

    @property
    def AuthorFull(self):
        return '%s <%s>' % (self._authorName, self._authorEmail)

    @property
    def Maintainer(self):
        return self._maintainerName

    @property
    def MaintainerContact(self):
        return self._maintainerEmail

    @property
    def MaintainerFull(self):
        return '%s <%s>' % (self._maintainerName, self._maintainerEmail)
