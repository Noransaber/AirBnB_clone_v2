#!/usr/bin/python3
""" module doc
"""
from fabric.api import task, local, env, put, run
from datetime import datetime
import os

env.hosts = ['52.206.189.175']


@task
def do_pack():
    """ method doc
        sudo fab -f 1-pack_web_static.py do_pack
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
    """ method doc
        fab -f 2-do_deploy_web_static.py do_deploy:
        archive_path=versions/web_static_20231004201306.tgz
        -i ~/.ssh/id_rsa -u ubuntu
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        tmp_archive_path = "/tmp/" + fn_with_ext

        # Upload the archive to the server
        put(archive_path, tmp_archive_path)

        # Create a new directory for the release
        run("mkdir -p {0}{1}".format(dpath, fn_no_ext))

        # Unpack the archive into the new directory
        run("tar -xzf {0} -C {1}{2}".format(tmp_archive_path, dpath, fn_no_ext))

        # Delete the temporary archive file
        run("rm {0}".format(tmp_archive_path))

        # Move the contents to the current directory
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))

        # Remove the old symbolic link and create a new one
        run("rm -rf /data/web_static/current")
        run("ln -s {0}{1}/ /data/web_static/current".format(dpath, fn_no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment error:", str(e))
        return False
