import os
import nox

nox.options.envdir = ".cache"

if os.name == 'nt':
    nox.options.default_venv_backend = "none"


@nox.session
def pylint(session):
    """Linter Score"""
    session.install("pylint")
    session.run("pylint", "newproject", "--output-format=parseable")
    #session.run("anybadge", "--value=10", "pylint")
