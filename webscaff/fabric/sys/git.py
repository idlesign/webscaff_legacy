from fabric.api import task, cd, run


@task
def clone(path_base, repo_url, dir_target):
    """Clones a remote repository."""
    with cd(path_base):
        run('git clone %s %s' % (repo_url, dir_target))


@task
def pull(path_base):
    """Pulls new data from a remote repository master branch.

    Any local changes will be lost.

    """
    with cd(path_base):
        run('git reset --hard')
        run('git pull origin master')
