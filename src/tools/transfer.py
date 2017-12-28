# coding: utf-8


from tools.common import exec_cmd_simple


class Transfer(object):

    def __init__(self):
        pass

    def send(self):
        pass


class RsyncTransfer(object):

    def __init__(self, src, dst, host):
        self.src = src
        self.dst = dst
        self.host = host

    def __str__(self):
        ret = ''
        host = self.host
        dst = self.dst
        if not isinstance(host, list):
            host = [host]
        if not isinstance(dst, list):
            dst = [dst]
        for h, d in zip(host, dst):
            ret += 'rsync -avz %s root@%s:%s ; \n' % (self.src, h, d)
        return ret

    def send(self):
        if None in [self.src, self.dst, self.host]:
            print "PLEASE CHECK YOUR PARAMETERS, IT IS SOME EMPTY!"
            return False
        return exec_cmd_simple(self.__str__())

    @staticmethod
    def send(src, dst):
        cmd = "rsync -avz %s %s" % (src, dst)
        return exec_cmd_simple(cmd)


class ScpTransfer(object):

    def __init__(self, src, dst, host):
        self.src = src
        self.dst = dst
        self.host = host

    def __str__(self):
        ret = ''
        src = self.src
        if not isinstance(src, list):
            src = [src]
        dst = self.dst
        if not isinstance(dst, list):
            dst = [dst]

        if len(src) > len(dst):
            print 'SCP: SRC > DST!'
            return None

        for i in range(len(src)):
            ret += 'scp %s root@%s:%s ;\n' % (src[i], self.host, dst[i])
        return ret

    @staticmethod
    def send(src, dst, host):
        cmd = "scp %s %s" % (src, dst)
        return exec_cmd_simple(cmd)

