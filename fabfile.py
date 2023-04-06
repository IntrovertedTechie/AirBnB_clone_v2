from fabric.api import local
from fabric.decorators import task

@task
def pack():
    archive_path = do_pack()
    if archive_path:
        print("Archive created at {}".format(archive_path))
    else:
        print("Archive creation failed")

