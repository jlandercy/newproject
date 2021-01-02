import os
import pathlib
import re
import subprocess

import nox
from lxml import etree

# Settings:

nox.options.envdir = ".cache"
nox.options.default_venv_backend = "none"

cache = pathlib.Path(nox.options.envdir)
cache.mkdir(exist_ok=True)

package = pathlib.Path(__file__).parent.parts[-1]
reports = pathlib.Path(nox.options.envdir) / 'reports'
reports.mkdir(exist_ok=True)


# Sessions:

@nox.session
def tests(session):
    """Package Test Suite Report"""
    report = reports / "tests.log"
    with report.open("w") as handler:
        session.run("python", "-m", "xmlrunner", "--output-file", str(reports / "tests.xml"),
                    "discover", "-v", f"{package:}.tests", stdout=handler)
    pattern = re.compile(r"Ran (?P<count>[\d]+) tests in (?P<elapsed>[.\d]+)s")
    count, elapsed = pattern.findall(report.read_text())[0]
    badge = reports / 'tests.svg'
    badge.unlink(missing_ok=True)
    session.run("anybadge", f"--value={count:}/{elapsed:}s", f"--file={badge:}", "--label=tests")


@nox.session
def linter(session):
    """Package Linter Score"""
    report = reports / "linter.log"
    with report.open("w") as handler:
        session.run(
            "pylint", package,
            "--output-format=parseable", "--rcfile=.pylintrc",
            "--fail-under=6", stdout=handler
        )
    pattern = re.compile(r"Your code has been rated at (?P<score>[-.\d]*)/10")
    score = float(pattern.findall(report.read_text())[0])
    badge = reports / 'linter.svg'
    badge.unlink(missing_ok=True)
    session.run("anybadge", f"--value={score:}/10", f"--file={badge:}", "--label=linter", "pylint")


@nox.session
def coverage(session):
    """Package Test Suite Coverage Score"""
    env = {"COVERAGE_FILE": str(reports / "coverage.dat")}
    report = reports / "coverage.xml"
    session.run("python", "-m", "coverage", "run", "-m", "unittest",
                "discover", "-v", f"{package:}.tests", env=env)
    session.run("python", "-m", "coverage", "report", "--omit=venv/**/*", env=env)
    session.run("python", "-m", "coverage", "xml", "-o", f"{report:}", env=env)
    with report.open() as handler:
        root = etree.XML(handler.read())
    score = float(root.get("line-rate"))*100.
    badge = reports / 'coverage.svg'
    badge.unlink(missing_ok=True)
    session.run("anybadge", f"--value={score:}%", f"--file={badge:}", "coverage")


@nox.session
def types(session):
    """Package Type Hints Report"""
    report = reports / "types.log"
    # Result of mypy is cached and differential:
    with report.open("w") as handler:
        session.run("python", "-m", "mypy",
                    "--cache-dir", str(reports.parent / ".mypy"),
                    "-v", package, stdout=handler)
    pattern = re.compile(r"Build finished in (?P<elapsed>[.\d]+) seconds "
                          "with (?P<modules>[\d]+) modules, "
                          "and (?P<errors>[\d]+) errors\n(?P<status>[\w]+): "
                          "no issues found in (?P<sources>[\d]+) source files")
    *_, status, files = pattern.findall(report.read_text())[0].lower()
    badge = reports / 'types.svg'
    badge.unlink(missing_ok=True)
    session.run("anybadge", f"--value={status:}", f"--file={badge:}", "--label=type-hints")


@nox.session
def styles(session):
    """Package Code Styles Report"""
    report = reports / "styles.log"
    with report.open("w") as handler:
        session.run("python", "-m", "isort", "--diff", ".", stdout=handler)#, success_codes=[0, 1])
        session.run("python", "-m", "black", "--check", "--diff", package,
                    stdout=handler, success_codes=[0, 1])
    pattern = re.compile(r"(?P<count>[\d]+) files would be reformatted")
    result = pattern.findall(report.read_text())
    badge = reports / 'styles.svg'
    badge.unlink(missing_ok=True)
    if result:
        count = result[0]
        session.run("anybadge", f"--value={count:}", f"--file={badge:}", "--color=red", "--label=code-style")
    else:
        session.run("anybadge", f"--value=black", f"--file={badge:}", "--color=black", "--label=code-style")


@nox.session
def notebooks(session):
    """Package Notebooks"""
    report = reports / "notebooks.log"
    with report.open("w") as handler:
        session.run("python", "-m", "ipykernel", "install", "--name=venv", stderr=handler)
        session.run(
            "python", "-m",
            "jupyter", "nbconvert", "--debug",
            "--ExecutePreprocessor.timeout=600",
            "--ExecutePreprocessor.kernel_name=venv",
            "--inplace", "--clear-output", "--to", "notebook",
            "--execute", "./docs/source/notebooks/*.ipynb",
            stderr=handler,
            success_codes=[0, 1]
        )
    with report.open() as handler:
        session.log(handler.read())
    pattern = re.compile(r"[NbConvertApp] Writing (?P<bytes>[\d]+) bytes to ")
    count = len(pattern.findall(report.read_text()))
    badge = reports / 'notebooks.svg'
    badge.unlink(missing_ok=True)
    session.run("anybadge", f"--value={count:}", f"--file={badge:}", "--label=notebooks",
                "1=red", "2=orange", "3=green")


@nox.session
def docs(session):
    """Package Documentation"""
    report = reports / "docs.log"
    with report.open("w") as handler:
        session.run("sphinx-build", "-b", "html", f"docs/source", str(cache / "docs"),
                    stdout=handler)
    pattern = re.compile(r"build (?P<status>[\w]+).")
    status = pattern.findall(report.read_text())[0]
    badge = reports / 'docs.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={status:}", f"--file={badge:}", "--label=docs")
