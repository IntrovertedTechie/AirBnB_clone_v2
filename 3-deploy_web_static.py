#!/usr/bin/python3
# a Fabric script that creates & distributes an archive to your web servers

from fabric.api import env, put, run, local
from datetime import datetime
from fabric import decorators
import os

env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = 'ubuntu'
env.key_filename = '/home/ubuntu/.ssh/school'


@decorators.runs_once
def do_pack():
    ''' generates a .tgz archive from the contents '''
    dt_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(dt_now)
    cmd_compress = "tar -cvzf {} web_static/".format(archive_path)
    local("mkdir -p versions")
    archived = local(cmd_compress)
    if archived.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    ''' distributes an archive to your web servers '''
    if os.path.isfile(archive_path) is False:
        return False
    put(archive_path, "/tmp")
    file_split = archive_path.split('/')
    file_w_ext = file_split[1]
    file_wo_ext = file_split[1].split('.')[0]
    if run("mkdir -p /data/web_static/releases/{}/".
           format(file_wo_ext)).failed is True:
        return False
    print("Release folder create done!")
    if run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".
           format(file_wo_ext, file_wo_ext)).failed is True:
        return False
    print("Uncompress the archive done!")
    if run("rm /tmp/{}".format(file_w_ext)).failed is True:
        return False
    print("Delete the archive done!")
    if run("mv /data/web_static/releases/{}/web_static/*"
           " /data/web_static/releases/{}/".
           format(file_wo_ext, file_wo_ext)).failed is True:
        return False
    print("Move all files and folders to one directory done!")
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(file_wo_ext)).failed is True:
        return False
    print("Delete empty folder web_static done!")
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    print("Delete the symbolic link done!")
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(file_wo_ext)).failed is True:
        return False
    print("Created new symbolic link done!")
    print("New version deployed!")
    return True


def deploy():
    ''' full deploy web_static files '''
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

