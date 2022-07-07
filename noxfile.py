# This file is part of cjdk-pre-commit.
# Copyright 2022 Board of Regents of the University of Wisconsin System
# SPDX-License-Identifier: MIT

import nox

nox.options.sessions = ["test"]


@nox.session(python=["3.8", "3.9", "3.10"])
def test(session):
    session.install(".[testing]")
    session.run("pytest")


@nox.session()
def systemtest(session):
    # Match the minimum version declared in .pre-commit-hooks.yaml.
    session.install("pre-commit == 2.0.0")
    session.install(".[testing]")
    session.run("pytest", "systemtests")
