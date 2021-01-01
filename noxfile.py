import re
import os
import pathlib
import subprocess

import nox
from lxml import etree


nox.options.envdir = ".cache"

if os.name == 'nt':
    nox.options.default_venv_backend = "none"


package = pathlib.Path(__file__).parent.parts[-1]
sink = pathlib.Path(nox.options.envdir) / 'reports'
sink.mkdir(exist_ok=True)


@nox.session
def pylint(session):
    """Linter Score"""
    report = sink / "pylint.log"
    with report.open("w") as output:
        session.run("pylint", package, "--output-format=parseable", "--fail-under=6", stdout=output)
    pattern = re.compile(r"Your code has been rated at (?P<score>[-.\d]*)/10")
    score = float(pattern.findall(report.read_text())[0])
    badge = sink / 'pylint.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={score:}/10", f"--file={badge:}", "pylint")


@nox.session
def coverage(session):
    """Coverage Score"""
    env = {"COVERAGE_FILE": str(sink / ".coverage")}
    report = sink / "coverage.xml"
    session.run("coverage", "run", "-m", "unittest", "discover", "-v", f"{package:}.tests", env=env)
    session.run("coverage", "report", "--omit=venv/**/*", env=env)
    session.run("coverage", "xml", "-o", f"{report:}", env=env)
    with report.open() as handler:
        root = etree.XML(handler.read())
    score = float(root.get("line-rate"))*100.
    badge = sink / 'coverage.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={score:}%", f"--file={badge:}", "coverage")
