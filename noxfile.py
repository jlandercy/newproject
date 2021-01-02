import re
import os
import pathlib
import subprocess

import nox
from lxml import etree


# Settings:

os.environ["PATH"] = r"c:\...\pywin32_system32;" + os.environ["PATH"]

nox.options.envdir = ".cache"
if os.name == 'nt':
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
    report = reports / "unittest.log"
    with report.open("w") as handler:
        session.run("python", "-m", "xmlrunner", "--output-file", str(reports / "unittest.xml"),
                    "discover", "-v", f"{package:}.tests", stdout=handler)
    pattern = re.compile(r"Ran (?P<count>[\d]+) tests in (?P<elapsed>[.\d]+)s")
    count, elapsed = pattern.findall(report.read_text())[0]
    badge = reports / 'unittest.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={count:}/{elapsed:}s", f"--file={badge:}", "--label=unittest")


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
    if badge.exists():
        badge.unlink()
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
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={score:}%", f"--file={badge:}", "coverage")


@nox.session
def typehints(session):
    """Package Type Hints Report"""
    report = reports / "typehints.log"
    # Result of mypy is cached and differential:
    with report.open("w") as handler:
        session.run("python", "-m", "mypy",
                    "--cache-dir", str(reports.parent / ".mypy"),
                    "-v", package, stdout=handler)
    pattern = re.compile(r"Build finished in (?P<elapsed>[.\d]+) seconds "
                          "with (?P<modules>[\d]+) modules, "
                          "and (?P<errors>[\d]+) errors\n(?P<status>[\w]+): "
                          "no issues found in (?P<sources>[\d]+) source files")
    *_, status, files = pattern.findall(report.read_text())[0]
    badge = reports / 'typehints.svg'
    if badge.exists():
        badge.unlink()
    session.run("anybadge", f"--value={status:}", f"--file={badge:}", "--label=type-hints")


@nox.session
def notebooks(session):
    """Package Notebooks"""
    report = reports / "notebooks.log"
    with report.open("w") as handler:
        session.run("python", "-m", "ipykernel", "install", "--name=venv")
        session.run(
            #"python", "-m",
            "jupyter", "nbconvert", "--debug",
            "--ExecutePreprocessor.timeout=600",
            "--ExecutePreprocessor.kernel_name=venv"
            "--inplace", "--clear-output", "--to", "notebook",
            "--execute", "./docs/source/notebooks/*.ipynb",
            stdout=handler
        )
    # pattern = re.compile(r"build (?P<status>[\w]+).")
    # status = pattern.findall(report.read_text())[0]
    # badge = reports / 'docs.svg'
    # if badge.exists():
    #     badge.unlink()
    # session.run("anybadge", f"--value={status:}", f"--file={badge:}", "--label=docs")


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
