import os

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authenticator
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

c.Authenticator.admin_users = {'ole', 'marco', 'martijn'}
c.Authenticator.whitelist = {'ole', 'user', 'marco', 'martijn'}
#c.LocalAuthenticator.create_system_users = True

#------------------------------------------------------------------------------
# PAMAuthenticator configuration
#------------------------------------------------------------------------------

# Authenticate local Linux/UNIX users with PAM

# The encoding to use for PAM
c.PAMAuthenticator.encoding = 'utf8'

# The PAM service to use for authentication.
c.PAMAuthenticator.service = 'login'

c.PAMAuthenticator.open_sessions = False

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

## Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
home_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
notebook_dir = home_dir + '/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
        'jupyterhub-user-{username}': home_dir,
        '/home/{username}/work': notebook_dir,
        '/home/ubuntu/data': {"bind": home_dir + '/data', "mode": "ro"},
        '/home/ubuntu/share': home_dir + '/share'
        }

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
