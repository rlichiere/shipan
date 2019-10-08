# -*- coding: utf-8 -*-


class _VersionLevel(object):

   def __init__(self):
      self._alpha = 'Alpha'
      self._beta = 'Beta'
      self._rc = 'ReleaseCandidate'
      self._release = 'Release'

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

VersionLevel = _VersionLevel()


class Version(object):

   def __init__(self, major, minor, build, level, revision, comment=None):
      self._major = major
      self._minor = minor
      self._build = build
      self._level = level
      self._revision = revision
      self._comment = comment

   @property
   def Version(self):
      return '%s.%s.%s' % (self._major, self._minor, self._build)

   @property
   def Revision(self):
      return '%s %s' % (self._level, self._revision)

   @property
   def VersionFull(self):
      return '%s %s' % (self.Version, self.Revision)
