#!/usr/bin/python3

"""
This module defines a function for deploying a web application to multiple servers.
"""

import os
from fabric.api import env, put, run

env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = 'ubuntu'
env.key_filename = '/home/ubuntu/.ssh/school'


def do_deploy(archive_path):
    """
    Deploy a web application to multiple servers.

    Args:
        archive_path (str): Path to the web application archive file.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        filename = os.path.basename(archive_path)
        foldername = '/data/web_static/releases/{}'.format(
            os.path.splitext(filename)[0])
        run('mkdir -p {foldername}'.format(foldername=foldername))
        run('tar -xzf /tmp/{filename} -C {foldername}'
            .format(filename=filename, foldername=foldername))
        run('rm /tmp/{filename}'.format(filename=filename))
        run('mv {foldername}/web_static/* {foldername}/'
            .format(foldername=foldername))
        run('rm -rf {foldername}/web_static'.format(foldername=foldername))
        run('rm -rf /data/web_static/current')
        run('ln -s {foldername} /data/web_static/current'
            .format(foldername=foldername))
        print('New version deployed!')
        return True
    except OSError as ex:
        print('Error: {}'.format(str(ex)))
        return False
