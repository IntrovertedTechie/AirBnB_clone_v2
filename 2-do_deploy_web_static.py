#!/usr/bin/env python3
"""Fabric script that distributes an archive to your web servers"""

import os
from fabric.api import *

env.hosts = [54.85.99.227, 100.25.198.209]


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_file)[0]
        archive_path_on_server = "/tmp/" + archive_file
        path_on_server = "/data/web_static/releases/" + archive_name

        put(archive_path, archive_path_on_server)
        run("mkdir -p {}".format(path_on_server))
        run("tar -xzf {} -C {}".format(archive_path_on_server, path_on_server))
        run("rm {}".format(archive_path_on_server))
        run("mv {}/web_static/* {}/".format(path_on_server, path_on_server))
        run("rm -rf {}/web_static".format(path_on_server))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_on_server))

        return True
    except:
        return False

