#!/usr/bin/env python3
"""Fabric script to create and distribute an archive to web servers"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = 'ubuntu'  
env.key_filename = '/home/ubuntu/.ssh/school'  # replace with your own SSH key path


def do_pack():
    """Creates a compressed archive of the web_static folder"""
    try:
        if not os.path.exists("versions"):
            os.mkdir("versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"versions/web_static_{now}.tgz"
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except:
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        file_no_ext = os.path.splitext(file_name)[0]
        # Upload archive to /tmp/ directory on both servers
        put(archive_path, "/tmp/")
        # Create target directory for deployment
        run("mkdir -p /data/web_static/releases/{}/".format(file_no_ext))
        # Extract archive contents to target directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, file_no_ext))
        # Delete the archive
        run("rm /tmp/{}".format(file_name))
        # Move symbolic link
        run("rm -f /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_no_ext))
        return True
    except:
        return False

def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

