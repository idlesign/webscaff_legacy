from fabric.api import task, sudo

from ..settings import PROJECT_NAME
from .nginx import stop, restart

__all__ = ['update']

@task
def update():
    """Updates SSL certificates using Let's Encrypt."""
    stop()
    sudo('/home/%s/letsencrypt/letsencrypt-auto renew --agree-tos' % PROJECT_NAME)
    restart()
