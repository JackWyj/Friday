# coding: utf-8


import yaml
from os import system


class CMD(object):

    def __init__(self, cmd, user, host):
        self.cmd = cmd
        self.user = user
        self.host = host

    def __str__(self):
        ret = self.cmd
        if self.user and self.host:
            ret = "ssh %s@%s '%s'" % (self.user, self.host, ret)
        return ret


class Mkdir(object):

    def __init__(self, ddir, user, host):
        self.dir = ddir
        self.user = user
        self.host = host

    def __str__(self):
        _ = self.dir
        if not isinstance(_, list):
            _ = [_]
        prefix = 'mkdir -p %s'
        if self.user and self.host:
            prefix = "ssh %s@%s " % (self.user, self.host) + " '%s' " % prefix

        return ';\n'.join([prefix % d for d in _])


class Rm(object):

    def __init__(self, f, user=None, host=None, force=False):
        self.file = f
        self.user = user
        self.host = host
        self.force = force

    def __str__(self):
        prefix = "rm %s %s"
        force = ''
        files = self.file
        if not isinstance(files, list):
            files = [files]
        if self.force:
            force = '-rf '
        if self.user and self.host:
            prefix = "ssh %s@%s " % (self.user, self.host) + " '%s' " % prefix

        return ';\n'.join([prefix % (force, f) for f in files])


def exec_cmd(cmd):
    print cmd
    code = system(cmd)
    if code != 0:
        print 'code: %s' % (code >> 8)
    return code


def exec_cmd_simple(cmd):
    if 0 == exec_cmd(cmd):
        return True
    return False


def chmod(filepath, a):
    return exec_cmd_simple("chmod %s %s" % (a, filepath))


def mkdir(filepath):
    return exec_cmd_simple('mkdir -p %s' % filepath)


def touch(filepath):
    return exec_cmd_simple('touch %s' % filepath)


def load_yaml(f):
    with open(f, 'r') as stream:
        try:
            conf = yaml.load(stream)
        except Exception, e:
            print e
            return None

    return conf


def write_file(content, filepath):
    print '----> write to %s' % filepath
    with open(filepath, 'w') as f:
        f.write(content)
        f.close()


def gen_bash_file(content, filepath):
    write_file(content, filepath)
    chmod(filepath, '+x')
