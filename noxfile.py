import re
import os
import pathlib
import subprocess

import nox

nox.options.envdir = ".cache"

if os.name == 'nt':
    nox.options.default_venv_backend = "none"


sink = pathlib.Path(nox.options.envdir) / 'reports'
sink.mkdir(exist_ok=True)


re_pylint = re.compile("Your code has been rated at (?P<score>[-.\d]*)/10")


@nox.session
def pylint(session):
    """Linter Score"""
    process = subprocess.run(
        ["pylint", "newproject", "--output-format=parseable"],
        capture_output=True,
        text=True,
    )
    session.log(process.stdout)
    score = float(re_pylint.findall(process.stdout)[0])
    session.run(
        "anybadge",
        "--value={}".format(score),
        "--file={}".format(sink / 'pylint.svg'),
        "pylint"
    )
