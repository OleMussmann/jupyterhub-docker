import os
import shlex
from dockerspawner import DockerSpawner

class FormSpawner(DockerSpawner):
    def _options_form_default(self):
        default_stack = "jupyter/minimal-notebook"
        default_env = "YOURNAME=%s\n" % self.user.name
        return """
	<br>
        <div class="form-group">
	    <label for="stack">Select your desired stack</label>
	    <select name="stack" size="1">
		<option value="jupyter/r-notebook">R: </option>
		<option value="jupyter/tensorflow-notebook">Tensorflow: </option>
		<option value="jupyter/datascience-notebook">Datascience: </option>
		<option value="jupyter/all-spark-notebook">Spark: </option>
		<option value="jupyterlab_img">Course: </option>
	    </select>
        </div>
        <div class="form-group">
            <label for="args">Extra notebook CLI arguments</label>
            <input name="args" class="form-control"
                placeholder="e.g. --debug"></input>
        </div>
        <div class="form-group">
            <label for="env">Environment variables (one per line)</label>
            <textarea class="form-control" name="env">{env}</textarea>
        </div>
        """.format(
            env=default_env,
	    stack=default_stack
        )

    def options_from_form(self, formdata):
        options = {}
        options['env'] = env = {}
        options['stack'] = formdata['stack']

        env_lines = formdata.get('env', [''])
        for line in env_lines[0].splitlines():
            if line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()

        arg_s = formdata.get('args', [''])[0].strip()
        if arg_s:
            options['argv'] = shlex.split(arg_s)
        image = ''.join(formdata['stack'])
        print("SPAWN: " + image + " IMAGE" )
        self.image = image
        return options

    def get_args(self):
        """Return arguments to pass to the notebook server"""
        argv = super().get_args()
        if self.user_options.get('argv'):
            argv.extend(self.user_options['argv'])
        return argv

    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        return env


#class FormSpawner(DockerSpawner):
#    def _options_form_default(self):
#        default_stack = "jupyter/minimal-notebook"
#        return """
#        <label for="stack">Select your desired stack</label>
#        <select name="stack" size="1">
#        <option value="jupyter/r-notebook">R: </option>
#        <option value="jupyter/tensorflow-notebook">Tensorflow: </option>
#        <option value="jupyter/datascience-notebook">Datascience: </option>
#        <option value="jupyter/all-spark-notebook">Spark: </option>
#        </select>
#        """.format(stack=default_stack)
#
#    def options_from_form(self, formdata):
#        options = {}
#        options['stack'] = formdata['stack']
#        image = ''.join(formdata['stack'])
#        print("SPAWN: " + image + " IMAGE" )
#        self.image = image
#        return options
#
c.JupyterHub.spawner_class = FormSpawner

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
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
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
