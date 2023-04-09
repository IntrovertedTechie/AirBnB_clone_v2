#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, local, run
from fabric.context_managers import lcd, cd
from datetime import datetime

env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = 'ubuntu'
env.key_filename = '/home/ubuntu/.ssh/school'


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    try:
        number = int(number)
    except:
        return None

    if number < 1:
        number = 1

    with lcd("versions"):
        local("ls -1t | tail -n +{} | xargs -I {} rm -- {}"
              .format(number + 1, "{}"))

    with cd("/data/web_static/releases"):
        run("ls -1t | tail -n +{} | xargs -I {} rm -rf -- {}"
            .format(number + 1, "{}"))


if __name__ == "__main__":
    do_clean()

