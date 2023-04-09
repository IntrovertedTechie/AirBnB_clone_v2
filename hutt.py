#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder and deploys it to a web server.
"""

from fabric.api import env, local, run
from fabric.context_managers import lcd, cd
from datetime import datetime

env.hosts = ['<IP address>']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Path of the .tgz archive if successful, None otherwise.
    """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Deploys the .tgz archive to a web server.

    Args:
        archive_path: Path of the .tgz archive to be deployed.

    Returns:
        True if successful, False otherwise.
    """
    if not archive_path:
        return False
    try:
        archive_file = archive_path.split("/")[-1]
        archive_name = archive_file.split(".")[0]
        remote_path = "/tmp/{}".format(archive_file)
        put(archive_path, remote_path)
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name))
        run("tar -xzf {} -C /data/web_static/releases/{}/"
            .format(remote_path, archive_name))
        run("rm {}".format(remote_path))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(archive_name, archive_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_name))
            return True
            except:
            return False
