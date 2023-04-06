from fabric.api import *
from datetime import datetime
import os

env.user = 'ubuntu'
efrom fabric.api import *
from datetime import datetime
import os

env.user = 'ubuntu'
env.key_filename = '/path/to/ssh/key'
env.hosts = ['54.85.99.227', '100.25.198.209']

def deploy():
    """Creates and distributes an archive to web servers using created function deploy and pack"""
    try:
        archive_path = do_pack()
    except Exception:
        return False

    if archive_path is None:
        return False

    return do_deploy(archive_path)

def do_pack():
    """Generates a .tgz archive from the contents of the web_static"""
    try:
        now = datetime.now()
        format_now = now.strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')

        archive_path = 'versions/web_static_{}.tgz'.format(format_now)
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Deploys archive file"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the archive filename without the extension
        archive_filename = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_filename)[0]

        # Create the destination directory on the web server
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_basename))

        # Uncompress the archive into the destination directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_basename))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the web_static directory to the destination directory
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(
                archive_basename, archive_basename))

        # Remove the empty web_static directory
        run('rmdir /data/web_static/releases/{}/web_static'.format(archive_basename))

        # Update the symbolic link to point to the new release
        run('rm -f /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(
            archive_basename))

        return True
    except:
        return False
nv.key_filename = '/path/to/ssh/key'
env.hosts = ['xx-web-01', 'xx-web-02']

def deploy():
    """Creates and distributes an archive to web servers using created function deploy and pack"""
    try:
        archive_path = do_pack()
    except Exception:
        return False

    if archive_path is None:
        return False

    return do_deploy(archive_path)

def do_pack():
    """Generates a .tgz archive from the contents of the web_static"""
    try:
        now = datetime.now()
        format_now = now.strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')

        archive_path = 'versions/web_static_{}.tgz'.format(format_now)
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Deploys archive file"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the archive filename without the extension
        archive_filename = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_filename)[0]

        # Create the destination directory on the web server
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_basename))

        # Uncompress the archive into the destination directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_basename))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the web_static directory to the destination directory
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(
                archive_basename, archive_basename))

        # Remove the empty web_static directory
        run('rmdir /data/web_static/releases/{}/web_static'.format(archive_basename))

        # Update the symbolic link to point to the new release
        run('rm -f /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(
            archive_basename))

        return True
    except:
        return False

