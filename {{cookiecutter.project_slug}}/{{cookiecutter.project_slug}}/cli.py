"""
Usage:  [OPTIONS] COMMAND [ARGS]...

  A cli for {{ cookiecutter.project_slug }}.

Options:
  --help  Show this message and exit.
"""
from pathlib import Path
import re
import os

import click


@click.group()
def main():
    """A cli for django-mako-plus."""
    pass


def get_main_helpstring(matchobj):
    """Return a programmatically-generated module-level docstring composed from main click entrypoint."""
    with click.Context(main) as ctx:
        return os.linesep.join(['"""', ctx.get_help(), '"""'])


# replace this module's docstring with the one generated from top-level cli entrypoint
current_module_text = Path(__file__).read_text()
with Path(__file__).open('w') as this_module:
    new_module_text = re.sub(
        re.compile(r'^"""(.*?)"""', re.DOTALL),
        get_main_helpstring,
        current_module_text
    )
    this_module.write(new_module_text)

if __name__ == "__main__":
    main()
