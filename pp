

#!/usr/bin/env python3
"""
Distributes an archive to your web servers using the function do_deploy.
"""

import os
from fabric.api import env, put, run

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'  # replace with your own username
env.key_filename = '/path/to/your/ssh/private/key'  # replace with your own SSH key path


def do_deploy(archive_path):
    """
    Uploads the archive to the /tmp/ directory of the web server,
    uncompresses the archive to the folder /data/web_static/releases/<archive filename without extension>,
    deletes the archive from the web server, deletes the symbolic link /data/web_static/current from the web server,
    creates a new symbolic link /data/web_static/current on the web server,
    linked to the new version of your code (/data/web_static/releases/<archive filename without extension>).
    Returns True if all operations have been done correctly, otherwise returns False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        filename = os.path.basename(archive_path)
        foldername = '/data/web_static/releases/' + os.path.splitext(filename)[0]
        run('mkdir -p {}'.format(foldername))
        run('tar -xzf /tmp/{} -C {}'.format(filename, foldername))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the folder to the parent folder
        run('mv {}/web_static/* {}/'.format(foldername, foldername))
        run('rm -rf {}/web_static'.format(foldername))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current on the web server,
        # linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run('ln -s {} /data/web_static/current'.format(foldername))

        print('New version deployed!')
        return True

    except Exception as e:
        print('Error: {}'.format(e))
        return False

