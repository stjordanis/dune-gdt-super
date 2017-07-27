#!/usr/bin/env python3

import os
import subprocess
import sys


cc_mapping = {'gcc': 'g++', 'clang': 'clang++'}
thisdir = os.path.dirname(os.path.abspath(__file__))

def update(commit, cc):
    gdt_super_dir = os.path.join(thisdir, '..', '..',)
    dockerfile = os.path.join(thisdir, 'dune-gdt-testing', 'Dockerfile')

    os.chdir(gdt_super_dir)

    cxx = cc_mapping[cc]
    commit = commit.replace('/', '_')
    repo = 'dunecommunity/dune-gdt-testing_{}'.format(cc)
    subprocess.check_call(['docker', 'build', '--no-cache=true', '-f', dockerfile,
                        '-t', '{}:{}'.format(repo, commit), '--build-arg', 'cc={}'.format(cc),
                        '--build-arg', 'cxx={}'.format(cxx), '--build-arg', 'commit={}'.format(commit),
                        '.'])
    subprocess.check_call(['docker', '--log-level="debug"', 'push', repo])

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ccs = [sys.argv[1]]
        commmits = [sys.argv[2]]
    else:
        ccs = list(cc_mapping.keys())
        commits = ['master']

    subprocess.check_call(['docker', 'pull', 'dunecommunity/testing-base:latest'])
    for b in commits:
        for c in ccs:
            update(b, c)
    subprocess.check_call(['docker', '--log-level="debug"', 'images'])
