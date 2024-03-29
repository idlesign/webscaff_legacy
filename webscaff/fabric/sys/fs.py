from fabric.api import task, sudo, run, local, put, hide
from fabric.contrib.files import append
from uuid import uuid4

from ..settings import PROJECT_USER, PROJECT_GROUP

__all__ = [
    'mkdir', 'chmod', 'set_owner', 'create_dir', 'gzip_dir', 'tail',
    'rm', 'append_to_file', 'touch', 'make_tmp_file']

@task
def mkdir(path, use_sudo=True):
    """Creates a directory."""
    command = sudo if use_sudo else run
    command('mkdir -p %s' % path)


@task
def chmod(path, mode):
    """Change fs object permissions."""
    sudo('chmod %s %s' % (mode, path))


@task
def set_owner(path, user, group):
    """Sets owner for path contents recursively."""
    sudo('chown -R %s:%s %s' % (user, group, path))


@task
def create_dir(path):
    """Prepares a directory (creates it and sets owner)."""
    mkdir(path)
    set_owner(path, PROJECT_USER, PROJECT_GROUP)


@task
def gzip_dir(src, target_fname, change_dir=None, do_sudo=False):
    """GZips a directory."""
    arch_ext = '.tar.gz'

    if arch_ext not in target_fname:
        target_fname = '%s%s' % (target_fname, arch_ext)

    change_dir = change_dir or ''
    if change_dir:
        change_dir = '-C %s' % change_dir

    command = sudo if do_sudo else run
    command('tar -czf %s %s %s' % (target_fname, change_dir, src))

    return target_fname


@task
def tail(fname):
    """Tails a file to output."""
    sudo('tail -f %s' % fname)


@task
def rm(target, force=True, use_local=True):
    """Removes target file or directory recursively."""
    command = local if use_local else sudo
    command('rm -r%s %s' % ('f' if force else '', target))


@task
def append_to_file(string, fpath):
    """Appends a string into file."""
    with hide('running'):
        append(fpath, string, use_sudo=True)


@task
def touch(fpath):
    """Creates a file or updates modified date if already exists."""
    run('touch %s' % fpath)


def make_tmp_file(contents):
    """Makes a temporary file with the given context."""
    fpath = '/tmp/wscf_%s' % uuid4()

    with open(fpath, 'w') as f:
        f.write(contents)

    append_to_file(contents, fpath)
    put(fpath, fpath, use_sudo=True)
    return fpath
