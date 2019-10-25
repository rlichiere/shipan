# -*- coding: utf-8 -*-
from tools import utils_exception as exc

from . import create_superuser


class History(object):

    def __init__(self):
        self._logs = list()
        self._hasFailed = False

    def add_log(self, label=None, failed=False, **result):
        # store log
        self._logs.append(HistoryLog(label=label, failed=failed, **result))

        if failed and not self._hasFailed:
            # switch on the `has_failed` property at first failure
            #  and avoid further updates
            self._hasFailed = True

    @property
    def has_failed(self):
        return self._hasFailed

    def get_logs(self):
        return self._logs

    def print_logs(self):
        _idx = 0
        for _log in self._logs:
            _idx += 1
            print('%02d. %s' % (_idx, _log.result_status_label, ))
            _label = ''
            if _log.label:
                _label += ': ' + _log.label

            _s = '{index}. {status}'.format(index=('%02d' % _idx), status=_log.result_status_label)
            if _log.label:
                _s += ': %s' % _log.label


class HistoryLog(object):

    def __init__(self, label=None, failed=False, **result):
        """
        :param failed:
        :type failed: bool
        :param result:
        :type result: **dict
        """
        self._label = label if label else ''
        self._success = not failed
        self._result = result

    @property
    def label(self):
        """
        :return:
        :rtype: bool
        """
        return self._label

    @property
    def success(self):
        """
        :return:
        :rtype: bool
        """
        return self._success

    @property
    def failed(self):
        """
        :return:
        :rtype: bool
        """
        return not self.success

    @property
    def result(self):
        """
        :return:
        :rtype: bool
        """
        return self._result

    @property
    def result_status_label(self):
        """
        :return:
        :rtype: str
        """
        return 'success' if self.success else 'error'


def install(**options):
    """
    Install the project according to given configuration.

    Steps performed during the installation process:

        1. Load the installer configuration

            Configuration can be done directly through the command parameters,
                otherwise via a command line wizard.

        2. Compile thesaurus (.mo) from translation files (.po)
            > python manage.py compilemessages

        3. Build potential Models migrations
            > python manage.py makemigrations

        4. Migrate Models
            > python manage.py migrate

        5. Create the superuser
            > python manage.py createsuperuser

        6. Create the potentially required cache table
            > python manage.py createcachetable

        7. Load models initial data
            > python manage.py populate

        8. Diagnose project
            > python manage.py diagnose

        9. Backup project
            > python manage.py backup

    :param options:
    :type options: **dict
    :return:
    :rtype: ?
    """
    _history = History()

    # compile thesaurus files

    # build potential migrations

    # migrate models

    # create superuser
    try:
        _admin = create_superuser(username=options['admin_username'],
                                  password=options['admin_password'],
                                  email=options['admin_email'],
                                  first_name=options['admin_first_name'],
                                  last_name=options['admin_last_name'],
                                  noinput=options['noinput'])
    except Exception as e:
        _history.add_log(failed=True, exc_type=exc.describe(e))
        return _history
    else:
        _history.add_log(label='create_superuser done. New client.id: #%s' % _admin.id, created_client=_admin)

    # potentially create the cache table

    # load models initial data

    # potentially diagnose project

    # potentially backup project

    return _history
