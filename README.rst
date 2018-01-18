=============================
Python 3 Package Cookiecutter
=============================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg

An opinionated, dead-simple cookiecutter_ for modern Python 3 packages.

*Adapted from Audrey's* cookiecutter-pypackage_


Features
--------

* Testing setup with ``py.test``
* Future-proof use of Pipfile_ as opposed to requirements.txt [see pipenv_]
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test
* Sphinx_ docs: Documentation ready for generation and hosting on `GitHub Pages`_
* Bumpversion_: Pre-configured version bumping with a single command
* Fabric_ for task automation
* Optional command line interface with Click_

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)

.. code-block:: bash

    brew install cookiecutter
    # or
    pip install -U cookiecutter
    # or
    pipenv install -d cookiecutter

Generate a Python package project

.. code-block:: bash

    cookiecutter https://github.com/knowsuchagency/cookiecutter-pypackage.git

    # answer questions to generate project template

    cd your_new_project
    pip install .[dev] # if using legacy Python tooling
    pipenv install -d # if using pipenv

    # to see what options are automated for you via fabric
    fab -l

Development
-----------

Upon creating your project and installing the requirements necessary for development, these are some of the options fabric_
will provide via the generated fabfile.

Prepend ``fab`` to the following commands from project root:

.. code-block:: bash

    clean                 Remove all build, test, coverage and Python artifacts.
    clean_build           Remove build artifacts.
    clean_pyc             Remove Python file artifacts.
    clean_test            Remove test and coverage artifacts.
    coverage              Check code coverage quickly with the default Python.
    dist                  Build source and wheel package.
    docs                  Generage Sphinx HTML documentation, including API docs.
    gen_requirements_txt  Generate a requirements.txt from Fabfile.
    publish_docs          Compile docs and publish to GitHub Pages.
    release               Package and upload a release to pypi.
    test                  Run tests quickly with default Python.
    test_all              Run on multiple Python versions with tox.
    tox                   Run on multiple Python versions with tox.
    verify_lockfile       Assert that all the packages in Pipfile are in Pipfile.lock


Upon pushing your project to github, I suggest immediately running

.. code-block:: bash

    fab publish_docs

and navigating to ``http://{your_github_username}.github.io/{repo_name}`` to witness your documentation
immediately rendered and available in all its glory. Cool stuff.

Additional Options
------------------

* Create a GitHub repo for your generated project.
* Add the repo to your Travis-CI_ account.
* Activate your project on `pyup.io`_.

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _PyPi: https://pypi.python.org/pypi
.. _`pipfile`: https://github.com/pypa/pipfile
.. _`fabric`: http://www.fabfile.org/
.. _`github pages`: https://pages.github.com/
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Click`: http://click.pocoo.org/
.. _`pipenv`: http://docs.pipenv.org/en/latest/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
