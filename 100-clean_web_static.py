#!/usr/bin/python3
""" Function that deploys """
from fabric.api import *


env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = "ubuntu"
env.key_filename = '/path/to/ssh/key'

def do_clean(number=0):
    """Deletes out-of-date archives"""

    number = int(number)

    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -d '\n' rm -rf --".format(number))

    path = '/data/web_static/releases'
    with cd(path):
        run("ls -t | tail -n +{} | xargs -d '\n' rm -rf --".format(number))

