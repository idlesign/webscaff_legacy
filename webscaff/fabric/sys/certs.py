from fabric.api import task, sudo

from ..settings import PROJECT_NAME


@task
def update():
    """Updates SSL certificates using Let's Encrypt."""
    sudo('/home/%s/letsencrypt/letsencrypt-auto renew --agree-tos' % PROJECT_NAME)
