import json
from configparser import ConfigParser
from functools import singledispatch
from pathlib import Path
from typing import List, NamedTuple

from click import secho
from fabric.api import abort, lcd, local, settings, task, warn_only
from fabric.tasks import Task


def _verify_lockfile():
    """Assert that all the packages in Pipfile are in Pipfile.lock"""

    class Packages(NamedTuple):
        default: List[str]
        development: List[str]

    config = ConfigParser()
    config.read('Pipfile')

    pipfile_packages = set(
        p.lower().replace('_', '-')
        for p, _ in config.items('packages') + (config.items(
            'dev-packages') if config.has_section('dev-packages') else []))

    for char in ['"', "'"]:
        pipfile_packages = set(p.replace(char, '') for p in pipfile_packages)

    lockfile_data = json.loads(Path('Pipfile.lock').read_text())
    lockfile_packages = set(
        tuple(lockfile_data['default'].keys()) +
        tuple(lockfile_data['develop'].keys()))

    assert pipfile_packages.issubset(
        lockfile_packages), \
        '{} package(s) in Pipfile not in Pipfile.lock - pipenv lock'. \
        format(pipfile_packages.difference(lockfile_packages))


@task
def clean_build():
    """Remove build artifacts."""
    local('rm -fr build/')
    local('rm -fr dist/')
    local('rm -rf .eggs/')
    local("find . -name '*.egg-info' -exec rm -fr {} +")
    local("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc():
    """Remove Python file artifacts."""
    local("find . -name '*.pyc' -exec rm -f {} +")
    local("find . -name '*.pyo' -exec rm -f {} +")
    local("find . -name '*~' -exec rm -f {} +")
    local("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_test():
    """Remove test and coverage artifacts."""
    local('rm -fr .tox/')
    local('rm -f .coverage')
    local('rm -fr htmlcov/')


@task
def clean():
    """Remove all build, test, coverage and Python artifacts."""
    clean_build()
    clean_pyc()
    clean_test()


@task
def dev_init():
    """Initialize clean development environment."""
    with warn_only():
        local("pipenv --rm")  # can fail
    local("pipenv install --dev")
    gen_requirements_txt.run()  # for zest.releaser


@task
def test(capture=True):
    """
    Run tests quickly with default Python.

    Args:
        capture: capture stdout [default: True]
    """
    disable_capturing = ' -s' if not true(capture) else ''
    verify_lockfile.run()
    local('py.test' + disable_capturing)


@task(alias='tox')
def test_all():
    """Run on multiple Python versions with tox."""
    local('tox')


@task
def coverage(open_browser=True):
    """Check code coverage quickly with the default Python."""
    local('coverage run --source {{ cookiecutter.project_slug }} -m pytest')
    local('coverage report -m')
    local('coverage html')
    if true(open_browser):
        local('open htmlcov/index.html')


@task
def docs(open_browser=True):
    """
    Generage Sphinx HTML documentation, including API docs.

    Args:
        open_browser: Open browser automatically after building docs
    """
    local('rm -f docs/{{ cookiecutter.project_slug }}.rst')
    local('rm -f docs/modules.rst')
    local('rm -f docs/{{ cookiecutter.project_slug }}*')
    local('sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}')

    with lcd('docs'):
        local('make clean')
        local('make html')

    local('cp -rf docs/_build/html/ public/')

    if true(open_browser):
        local('open public/index.html')


@task
def publish_docs():
    """
    Compile docs and publish to GitHub Pages.

    Logic borrowed from `hugo <https://gohugo.io/tutorials/github-pages-blog/>`
    """
    from textwrap import dedent

    with settings(warn_only=True):
        if local('git diff-index --quiet HEAD --').failed:
            local('git status')
            abort(
                'The working directory is dirty. Please commit any pending changes.'
            )

        if local('git show-ref refs/heads/gh-pages').failed:
            # initialized github pages branch
            local(
                dedent("""
                git checkout --orphan gh-pages
                git reset --hard
                git commit --allow-empty -m "Initializing gh-pages branch"
                git push gh-pages
                git checkout master
                """).strip())
            secho('created github pages branch', fg='green')

    # deleting old publication
    local('rm -rf public')
    local('mkdir public')
    local('git worktree prune')
    local('rm -rf .git/worktrees/public/')
    # checkout out gh-pages branch into public
    local('git worktree add -B gh-pages public gh-pages')
    # generating docs
    docs(open_browser=False)
    # push to github
    with lcd('public'), settings(warn_only=True):
        local('git add .')
        local('git commit -m "Publishing to gh-pages (Fabfile)"')
        local('git push origin gh-pages')


@task
def dist():
    """Build source and wheel package."""
    clean()
    local('python setup.py sdist')
    local('python setup.py bdist_wheel')


@task
def release():
    """Package and upload a release to pypi."""
    clean()
    test_all()
    publish_docs()
    local('python setup.py sdist upload')
    local('python setup.py bdist_wheel upload')


@task
def gen_requirements_txt(with_dev=False):
    """
    Generate a requirements.txt from Pipfile.lock

    This is more for the benefit of third-party packages
    like pyup.io that need requirements.txt
    """
    out = local('pipenv lock -r', capture=True)
    with open("requirements.txt", "w") as requirements:
        requirements.write(out.stdout)
    secho('succesfully generated requirements.txt', fg='green')
    if with_dev:
        out = local('pipenv lock -d -r', capture=True)
        with open("test-requirements.txt", "w") as requirements:
            requirements.write(out.stdout)
        secho('succesfully generated test-requirements.txt', fg='green')


class VerifyLockfile(Task):
    name = 'verify_lockfile'

    def set_docstring(func):
        func.__doc__ = _verify_lockfile.__doc__
        return func

    @set_docstring
    def run(self):
        _verify_lockfile()
        secho('lockfile verified', fg='green')


verify_lockfile = VerifyLockfile()
verify_lockfile.__doc__ = _verify_lockfile.__doc__


@singledispatch
def true(arg):
    """
    Determine of the argument is True.

    Since arguments coming from the command line
    will always be interpreted as strings by fabric
    this helper function just helps us to do what is
    expected when arguments are passed to functions
    explicitly in code vs from user input.

    Just make sure NOT to do the following with task arguments:

    @task
    def foo(arg):
        if arg: ...

    Always wrap the conditional as so

    @task
    def foo(arg):
        if true(arg): ...

    and be aware that true('false') -> False

    Args:
        arg: anything

    Returns: bool

    """
    return bool(arg)


@true.register(str)
def _(arg):
    """If the lowercase string is 't' or 'true', return True else False."""
    argument = arg.lower().strip()
    return argument == 'true' or argument == 't'
