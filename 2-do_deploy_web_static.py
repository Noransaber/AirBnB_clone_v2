#!/usr/bin/python3
"""
    Distributes an archive to your web servers,
    using the function do_deploy
    def do_deploy(archive_path):
    Return False iff archive path doesn't exist
"""

from fabric.api import env, local, put, run

# Define the list of web servers
env.hosts = ['xx-web-01', 'xx-web-02']

# Define the function to deploy an archive to a web server
def do_deploy(archive_path):
  """Deploys an archive to a web server.

  Args:
    archive_path: The path to the archive file.

  Returns:
    True if the deployment was successful, False otherwise.
  """

  # Check if the archive file exists.
  if not local.path.exists(archive_path):
    return False

  # Upload the archive file to the web server.
  put(archive_path, '/tmp/')

  # Uncompress the archive file on the web server.
  run('mkdir -p /data/web_static/releases/{}'.format(archive_path.split('/')[-1].split('.')[0]))
  run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(archive_path, archive_path.split('/')[-1].split('.')[0]))

  # Delete the archive file from the web server.
  run('rm /tmp/{}'.format(archive_path))

  # Delete the symbolic link `/data/web_static/current` from the web server.
  run('rm -rf /data/web_static/current')

  # Create a new symbolic link `/data/web_static/current` on the web server,
  # linked to the new version of the code.
  run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(archive_path.split('/')[-1].split('.')[0]))

  return True

# Deploy the archive to all web servers.
if __name__ == '__main__':
  for host in env.hosts:
    if not do_deploy(archive_path):
      print('Failed to deploy archive to {}'.format(host))
      exit(1)

  print('Archive successfully deployed to all web servers.')
