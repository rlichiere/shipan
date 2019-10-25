# -*- coding: utf-8 -*-
import os
import markdown2


from django.contrib import messages
from django.template import loader
from django.views.generic import View
from django.shortcuts import HttpResponse, redirect, reverse
from django.utils.translation import gettext as _

from shipan import config

from tools import utils_views


class DocHierarchy(object):

    def __init__(self, root_path, load_now=False):
        self._rootPath = root_path
        self._hierarchyData = None
        if load_now:
            self.load()

    def load(self):
        _filesList = dict()

        for _root, _dirs, _files in os.walk(self._rootPath):
            for _fileName in _files:
                if _fileName[-3:] == '.md':
                    _vRoot = _root[len(self._rootPath):]

                    if config.RUNNING_ON_WINDOWS:
                        _vRoot = _vRoot.replace('\\', '/')
                        _filePath = _root + '\\' + _fileName
                    else:
                        _filePath = _root + '/' + _fileName

                    _vFilePath = '/doc' + _vRoot + '/' + _fileName
                    try:
                        with open(_filePath, 'r') as _file:
                            _pageTitle = _file.readline()
                    except IOError:
                        continue
                    _pageTitle = _pageTitle.replace('# ', '')

                    _filesList[_vFilePath] = {
                        'file_name': _fileName,
                        'page_title': _pageTitle,
                        'parent_path': _root,
                    }
        self._hierarchyData = _filesList

    def clear(self):
        self._hierarchyData = None

    def get_config(self, path):
        return self._hierarchyData[path]

    def get_config_key(self, path, key):
        return self._hierarchyData[path][key]

    def set_config_key(self, path, key, value):
        self._hierarchyData[path][key] = value

    def has_path(self, path):
        return self._hierarchyData.has_key(path)

    def get_rendered(self, path):
        return self._hierarchyData[path]['rendered']

    def load_path(self, vpath, path):
        try:
            with open(path, 'r') as _file:
                _fileContent = _file.read()
                self.set_config_key(vpath, 'file_content', _fileContent)
        except IOError:
            return False

        return True

    def render_path(self, vpath, path):
        _rendered = self.render(path)
        self.set_config_key(vpath, 'rendered', _rendered)

    def get_toc(self):
        _toc = [{'path': _k, 'title': _v['page_title']} for _k, _v in self._hierarchyData.iteritems()]
        return _toc

    @staticmethod
    def render(path):
        return markdown2.markdown_path(path, extras=["fenced-code-blocks"])

docHierarchy = DocHierarchy(root_path=r'%s\doc' % config.settings.BASE_DIR, load_now=True)


class DocPage(utils_views.SuperuserRequiredMixin, View):
    template_name = 'doc/doc_page.html'

    def get(self, request, **kwargs):
        _vpath = kwargs.get('path', None)

        context = dict()
        context['request'] = request

        if _vpath is None:
            # home
            _homeContent = '<h1>%(home)s</h1>' % {'home': _('PAGE_DOCUMENTATION_HOME_TITLE')}
            _homeContent += '<ul>'
            for _tocItem in docHierarchy.get_toc():
                _homeContent += '<li><a href="' + _tocItem['path'] + '">' + _tocItem['title'] + '</a></li>'
            _homeContent += '</ul>'
            context['page_content'] = _homeContent
            context['page_is_home'] = True
        else:
            # some doc page
            if config.RUNNING_ON_WINDOWS:
                _path = r'%s\doc\%s' % (config.settings.BASE_DIR, _vpath.replace('/', '\\'))
            else:
                _path = r'%s\doc\%s' % (config.settings.BASE_DIR, _vpath)

            _vpath = '/doc/' + _vpath
            if not docHierarchy.load_path(_vpath, _path):

                messages.error(self.request, message=_('ERROR_WHILE_LOADING_DOCUMENTATION_FILE'))
                return redirect(reverse('fo-home'))

            docHierarchy.render_path(_vpath, _path)

            # load markdown file and transform it to html
            _rendered = docHierarchy.get_rendered(_vpath)

            context['page_content'] = _rendered
        _template = loader.get_template(self.template_name)
        _htmlPage = _template.render(context)

        return HttpResponse(_htmlPage)