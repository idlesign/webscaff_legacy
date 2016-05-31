from os import path

from .settings import PATH_LOCAL_PROJECT_BASE, PATH_REMOTE_PROJECT_BASE


def get_paths(sub):
    """Returns local and remote paths tuple for a given project file/dir.

    :param sub:

    """
    return (path.join(PATH_LOCAL_PROJECT_BASE, sub),
            path.join(PATH_REMOTE_PROJECT_BASE, sub))


def get_symlink_command(from_file, dest):
    """Returns a symlink command.

    :param from_file:
    :param dest:

    """
    return 'ln -sf %s %s' % (from_file, dest)
