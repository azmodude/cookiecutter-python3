#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup

from pip.req import parse_requirements

requirements = [
    str(r.req) for r in parse_requirements('requirements.txt', session=False)
]
test_requirements = [
    str(r.req)
    for r in parse_requirements('test-requirements.txt', session=False)
]

setup(
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={
        'dev': test_requirements,
        'development': test_requirements,
        'test': test_requirements,
        'testing': test_requirements
    },
{% if cookiecutter.cli.lower() == 'y' or cookiecutter.cli.lower() == 'yes' -%}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main'
        ]
},
{% endif -%}
)
