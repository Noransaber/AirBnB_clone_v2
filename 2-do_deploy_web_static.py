from fabric.api import env, put, run
from datetime import datetime
from os.path import exists, isdir

def do_deploy(archive_path):
  """
  Deploys an archive to the web servers.

  Args:
    archive_path: The path to the archive file.

  Returns:
    True if the deployment was successful, False otherwise.
  """

  if not exists(archive_path):
    return False

  # Upload the archive to the /tmp/ directory of the web server
  put(archive_path, '/tmp/')

  # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
  file_n = archive_path.split("/")[-1]
  no_ext = file_n.split(".")[0]
  path = "/data/web_static/releases/"
  run('mkdir -p {}{}/'.format(path, no_ext))
  run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

  # Delete the archive from the web server
  run('rm /tmp/{}'.format(file_n))

  # Delete the symbolic link /data/web_static/current from the web server
  run('rm -rf /data/web_static/current')

  # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
  run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

  return True

# Set the hosts to deploy to
env.hosts = ['xx-web-01', 'xx-web-02']

# Deploy the archive
def deploy():
  archive_path = 'versions/web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))

  if not do_deploy(archive_path):
    print('Deployment failed.')
    return

  print('Deployment successful.')

if __name__ == '__main__':
  deploy()
