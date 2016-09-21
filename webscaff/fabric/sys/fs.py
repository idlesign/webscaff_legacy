from fabric.api import task, sudo, run, local

from ..settings import PROJECT_USER, PROJECT_GROUP


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
def gzip_dir(src, target_fname, change_dir=None):
    """GZips a directory."""
    arch_ext = '.tar.gz'

    if arch_ext not in target_fname:
        target_fname = '%s%s' % (target_fname, arch_ext)

    change_dir = change_dir or ''
    if change_dir:
        change_dir = '-C %s' % change_dir

    run('tar -czf %s %s %s' % (target_fname, change_dir, src))

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
    sudo('echo %s >> %s' % (string, fpath))


@task
def touch(fpath):
    """Creates a file or updates modified date if already exists."""
    run('touch %s' % fpath)
