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


@nox.session
def pylint(session):
    """Linter Score"""
    process = subprocess.run(
        ["pylint", "newproject", "--output-format=parseable"],
        capture_output=True,
        encoding='utf-8'
    )
    session.log(" ".join(process.args))
    session.log(process.stdout)
    pattern = re.compile(r"Your code has been rated at (?P<score>[-.\d]*)/10")
    score = float(pattern.findall(process.stdout)[0])
    badge = sink / 'pylint.svg'
    if badge.exists():
        badge.unlink()
    session.run(
        "anybadge",
        "--value={}".format(score),
        "--file={}".format(badge),
        "pylint"
    )


@nox.session
def coverage(session):
    """Coverage Score"""
    env = {"COVERAGE_FILE": str(sink / ".coverage")}
    session.run("coverage", "run", "-m", "unittest", "discover", "-v", "newproject.tests", env=env)
    session.run("coverage", "report", "--omit=venv/**/*", env=env)
    session.run("coverage", "xml", "-o", str(sink / "coverage.xml"), env=env)
    # pattern = re.compile(r"Your code has been rated at (?P<score>[-.\d]*)/10")
    # score = float(pattern.findall(process.stdout)[0])
    # badge = sink / 'pylint.svg'
    # if badge.exists():
    #     badge.unlink()
    # session.run(
    #     "anybadge",
    #     "--value={}".format(score),
    #     "--file={}".format(badge),
    #     "pylint"
    # )
