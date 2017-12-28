# coding: utf-8


class Job(object):

    def __init__(self):
        self.name = 'JOB'

    def start(self, _):
        pass

    def stop(self, _):
        pass

    def run(self, params):
        self.start(params)

    def print_process(self, _):
        pass

