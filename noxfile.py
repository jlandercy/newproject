import re
import os
import pathlib

import nox
from lxml import etree


nox.options.envdir = ".cache"

if os.name == 'nt':
    nox.options.default_venv_backend = "none"


package = pathlib.Path(__file__).parent.parts[-1]
reports = pathlib.Path(nox.options.envdir) / 'reports'
reports.mkdir(exist_ok=True)


@nox.session
def tests(session):
    """Test Suite"""
    session.run("python", "-m", "xmlrunner", "--output-file", str(reports / "unittest.xml"),
                "discover", "-v", f"{package:}.tests")
    report = reports / "unittest.log"
    with report.open("w") as handler:
        session.run("python", "-m", "unittest", "discover", "-v", f"{package:}.tests", stdout=handler)
    pattern = re.compile(r"Ran (?P<count>[\d]+) tests in (?P<elapsed>[.\d]+)s")
    count, elapsed = pattern.findall(report.read_text())[0]
    badge = reports / 'unittest.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={count:}/{elapsed:}s", f"--file={badge:}", "--label=unittest")


@nox.session
def linter(session):
    """Linter Score"""
    report = reports / "pylint.log"
    with report.open("w") as handler:
        session.run(
            "pylint", package,
            "--output-format=parseable", "--rcfile=.pylintrc",
            "--fail-under=6", stdout=handler
        )
    pattern = re.compile(r"Your code has been rated at (?P<score>[-.\d]*)/10")
    score = float(pattern.findall(report.read_text())[0])
    badge = reports / 'pylint.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={score:}/10", f"--file={badge:}", "pylint")


@nox.session
def coverage(session):
    """Coverage Score"""
    env = {"COVERAGE_FILE": str(reports / ".coverage")}
    report = reports / "coverage.xml"
    session.run("coverage", "run", "-m", "unittest", "discover", "-v", f"{package:}.tests", env=env)
    session.run("coverage", "report", "--omit=venv/**/*", env=env)
    session.run("coverage", "xml", "-o", f"{report:}", env=env)
    with report.open() as handler:
        root = etree.XML(handler.read())
    score = float(root.get("line-rate"))*100.
    badge = reports / 'coverage.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={score:}%", f"--file={badge:}", "coverage")

