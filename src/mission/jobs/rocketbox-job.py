# coding: utf-8


from os.path import basename
from mission.job import Job
from tools.transfer import (
    RsyncTransfer,
    ScpTransfer
)
from tools.common import (
    Rm,
    CMD,
    chmod,
    mkdir,
    touch,
    Mkdir,
    write_file,
    gen_bash_file,
    exec_cmd_simple,
)


class Rocketbox(Job):

    def __init__(self):
        self.name = 'Rocketbox'

    def prepare(self, p):
        ffile, fscript = self.get_tmp_dir(p['tmp_dir'])
        mkdir(ffile)
        mkdir(fscript)
        files = []
        i = 0
        for t in p.get('transit'):
            filepath = fscript + str(i) + t['node'] + '.sh'
            touch(filepath)
            chmod(filepath, '+x')
            files.append(filepath)
            i += 1
        return files

    def get_tmp_dir(self, ddir):
        return ddir + '/file/', ddir + '/script/'

    def post(self, bash):
        i = 0
        for n, c in bash:
            write_file(c, n)
            i += 1

    def start(self, params):

        transit = params.get('transit', [])
        src_file = params.get('src_file')
        dst_file = params.get('dst_file')
        target = params.get('target')

        local_node = {'node': 'localhost',
                      'tmp_dir': params.get('tmp_dir')}
        transit.insert(0, local_node)
        local_bash = self.prepare(params)

        i = 1
        num = len(local_bash)
        final_bash = []
        for cur, nxt in zip(transit, transit[1:]):

            tfile, tscript = self.get_tmp_dir(nxt['tmp_dir'])
            mkdir_cmd = Mkdir([tfile, tscript], 'root', nxt['node']).__str__()

            scp_cmd = ''
            if i < num:
                cp_src_file = [cur['tmp_dir'] + '/script/' + basename(f) for f in local_bash[i:]]
                cp_dst_file = [tscript + basename(f) for f in local_bash[i:]]
                scp_cmd = ScpTransfer(cp_src_file, cp_dst_file, nxt['node']).__str__()

            src_dir = cur['tmp_dir'] + '/file/'
            if cur['node'] == 'localhost':
                src_dir = src_file
            dst_dir = tfile
            rsync_cmd = RsyncTransfer(src_dir, dst_dir, nxt['node']).__str__()

            exe_cmd = ''
            if i < num:
                dst_script = tscript + basename(local_bash[i])
                exe_cmd = CMD("/bin/sh %s" % dst_script, 'root', nxt['node']).__str__()

            if cur['node'] != 'localhost':
                rm_cmd = Rm(src_dir, force=True).__str__()
            else:
                rm_cmd = Rm(cur['tmp_dir'], force=True).__str__()

            cmds = [mkdir_cmd, scp_cmd, rsync_cmd, exe_cmd]
            if rm_cmd:
                cmds.append(rm_cmd)

            cmd = '\n'.join(cmds)
            final_bash.append((cur['node'], cmd))
            i += 1

        node = transit[-1]
        src_dir = node['tmp_dir'] + '/file/'
        if node['node'] == 'localhost':
            src_dir = src_file
        rm_cmd = Rm(node['tmp_dir'], force=True).__str__()

        cmd = '\n'.join([RsyncTransfer(src_dir, [t['dst_file'] for t in target],
                                       [t['node'] for t in target]).__str__(), rm_cmd])
        final_bash.append((node['node'], cmd))

        _, local_tmp = self.get_tmp_dir(params.get('tmp_dir'))
        scripts = []
        i = 0
        for f in final_bash:
            n, c = f[0], f[1]
            scripts.append((local_tmp + str(i) + n + '.sh', c))
            print "======: %s" % n
            print c
            i += 1

        self.post(scripts)
        ans = raw_input("Are you SURE to trigger the bash scripts generated by me? [Y/n]")
        if ans == 'Y':
            return exec_cmd_simple('/bin/sh %s' % scripts[0][0])
        return True

    def run(self, conf):
        return self.start(conf)





