from fabric.api import task

@task
def do_deploy(archive_path):
    """Deploy the web static archive to the production server."""

    # Create a temporary directory on the production server.
    temp_dir = run("mktemp -d")

    # Upload the web static archive to the production server.
    put(archive_path, temp_dir)

    # Extract the web static archive on the production server.
    run("tar -xvzf {} -C {}".format(temp_dir, "/var/www/html"))

    # Remove the temporary directory on the production server.
    run("rm -rf {}".format(temp_dir))
