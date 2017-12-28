# coding: utf-8


import yaml


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

