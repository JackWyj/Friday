# coding: utf-8


import re
import imp
from os import (
    listdir,
    getcwd
)
from os.path import join
from tools.error import (
    ALL_SUCCESS,
    ALL_FAIL,
    PART_SUCCESS
)
from tools.file_tools import load_yaml


class JobEngine:

    def __init__(self):
        self.name = 'JobEngine'
        self.path = join(getcwd(), 'mission/jobs')
        self.suffix = ('.py', '.yaml')
        self.object_item = 'object'
        self.load_item = 'load'

    def handle_error_num(self, real, std):
        if std == 0 or real == 0:
            return ALL_SUCCESS
        if real < std:
            return PART_SUCCESS
        return ALL_FAIL

    def _call_plugins(self, plugins):
        if not plugins or not isinstance(plugins, dict):
            return ALL_FAIL

        for k in plugins.get('yaml', {}).keys():

            c = load_yaml(plugins['yaml'][k])
            if c is None:
                self.log('Failed to load conf [%s]' % plugins['yaml'][k])
            if c.get('ignore'):
                self.log('Ingore [%s]' % k)
                continue

            self.log('Load [%s] for [%s]' % (c[self.load_item], k))
            mod = imp.load_source(c[self.object_item], plugins['py'][c[self.load_item]])
            cls = getattr(mod, c[self.object_item])()
            ret = cls.run(c)
            if not ret:
                self.log('Failed to run plugin [%s] !' % k)
        return None

    def _detect_files(self):
        return [join(self.path, f) for f in listdir(self.path)
                if f.endswith(self.suffix)]

    def _handle_files(self, files):
        c = '\/(?P<name>[\w-]+)\.(?P<type>py|yaml)?'
        ret = {}
        for f in files:
            m = re.search(c, f)
            if not m:
                continue

            name, ty = m.group('name'), m.group('type')
            if name == '__init__':
                continue
            if ty not in ret:
                ret[ty] = {}
            ret[m.group('type')][name] = f
        return ret

    def load_plugins(self):
        return self._call_plugins(self._handle_files(self._detect_files()))

    def run(self):
        ret = self.load_plugins()
        self.log({ALL_FAIL: 'All failed!',
                  ALL_SUCCESS: 'All succeed!',
                  PART_SUCCESS: 'Partly succeed!'}.get(ret, 'Nothing.'))

    @staticmethod
    def log(msg):
        print msg




