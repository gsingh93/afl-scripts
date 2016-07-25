#!/usr/bin/env python2

import os
import subprocess
import shutil
import libafl

project_dir = os.path.dirname(os.path.realpath(__file__))

class LibarchiveProject(libafl.AflProject):
    def __init__(self, wrapper=None):
        super(LibarchiveProject, self).__init__(wrapper)

        self.addTarget('afl', LibarchiveAflTarget('input', 'output', './libarchivetest-afl', '@@'))
        self.addTarget('debug', LibarchiveDebugTarget())

class LibarchiveDebugTarget(libafl.Target):
    root_path = project_dir
    src_dir = 'libarchive-debug'

    def init(self):
        if not os.path.isdir(self.src_dir):
            subprocess.check_output(['tar', '-xf', 'libarchive-3.2.1.tar.gz'])
            shutil.move('libarchive-3.2.1', self.src_dir)

    def build(self):
        subprocess.check_output(
            './configure --without-lzma --without-xml2 && make',
            shell=True,
        )
        os.chdir(self.root_path);
        subprocess.check_output(
            ('gcc libarchivetest.c %s/.libs/libarchive.a -I %s/libarchive ' +
            '-lz -lssl -lcrypto -lexpat -lxml2 -ldl -o libarchivetest-afl') %
            (self.src_dir, self.src_dir),
            shell=True,
        )

class LibarchiveAflTarget(libafl.AflTarget):
    root_path = project_dir
    src_dir = 'libarchive-afl'

    def __init__(self, *args, **kwargs):
        super(LibarchiveAflTarget, self).__init__(*args, **kwargs)

    def init(self):
        if not os.path.isdir(self.src_dir):
            subprocess.check_output(['tar', '-xf', 'libarchive-3.2.1.tar.gz'])
            shutil.move('libarchive-3.2.1', self.src_dir)

    def build(self):
        envs = self.set_afl_envs(cc='afl-gcc')
        env = dict(os.environ, **envs)
        subprocess.check_output(
            './configure --without-lzma --without-xml2 && make',
            shell=True,
            env=env,
        )
        os.chdir(self.root_path);
        subprocess.check_output(
            ('afl-gcc libarchivetest.c %s/.libs/libarchive.a -I %s/libarchive ' +
            '-lz -lssl -lcrypto -lexpat -lxml2 -ldl -o libarchivetest-afl') %
            (self.src_dir, self.src_dir),
            shell=True,
            env=env,
        )

    def clean(self):
        return 'make clean'

if __name__ == '__main__':
    libafl.handle_args(LibarchiveProject(libafl.TmuxWrapper()))
