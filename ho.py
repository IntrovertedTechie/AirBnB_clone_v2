#!/usr/bin/python3
import os
from fabric.api import env, put, run

env.hosts = ['54.85.99.227', '100.25.198.209']
env.user = 'ubuntu'
env.key_filename = '/home/ubuntu/.ssh/school'  

def do_deploy(archive_path):
       if not os.path.exists(archive_path):
        return False
    try:
         put(archive_path, '/tmp/')                 filename = os.path.basename(archive_path)
        foldername = '/data/web_static/releases/{}'.format(os.path.splitext(filename)[0])
        run('mkdir -p {}'.format(foldername))
        run('tar -xzf /tmp/{} -C {}'.format(filename, foldername))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}/'.format(foldername, foldername))
        run('rm -rf {}/web_static'.format(foldername))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(foldername))
        print('New version deployed!')
        return True
    except Exception as ex:
        print('Error: {}'.format(str(ex)))
        return False

