# -*- coding: utf-8 -*-
"""Top-level package for {{ cookiecutter.project_name }}."""

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except AttributeError:
    __version__ = 'unknown'

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'
