from os import path, getcwd

from fabric.api import env


USER = env.user
PASSWORD = env.password

HOST = env.host
PROJECT_NAME = env.project_name

GIT_REPO = env.git_repo
GIT_REPO_EXTENDED = bool(getattr(env, 'repo_extended', False))

WEBSERVER_USER = getattr(env, 'webserver_user', 'www-data')

PROJECT_USER = PROJECT_NAME
PROJECT_GROUP = PROJECT_USER

PATH_TEMP = '/tmp'
PATH_PYTHON = '/usr/bin/python3'

PATH_REMOTE_PROJECT_BASE = '/var/www/%s/' % PROJECT_NAME
PATH_REMOTE_PROJECT = path.join(PATH_REMOTE_PROJECT_BASE, PROJECT_NAME)

PATH_LOCAL_PROJECT_BASE = getcwd()
PATH_LOCAL_PROJECT = path.join(PATH_LOCAL_PROJECT_BASE, PROJECT_NAME)

NAME_CONFIGS_DIR = 'conf'

PATH_GIT_ROOT = PATH_REMOTE_PROJECT_BASE if GIT_REPO_EXTENDED else PATH_REMOTE_PROJECT

env.hosts = ['%s@%s' % (USER, HOST)]
