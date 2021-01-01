import nox


@nox.session(python=False)
def pylint(session):
    session.install("pylint")
    session.run("pylint", "newproject")
