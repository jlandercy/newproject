import nox

@nox.session
def pylint(session):
    session.install("pylint")
    session.run("pylint", "newproject")
