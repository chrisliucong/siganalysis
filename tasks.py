# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 The siganalysis developers. All rights reserved.
# Project site: https://github.com/questrail/siganalysis
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Invoke based tasks for siganalysis
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from invoke import run, task
from unipath import Path

ROOT_DIR = Path(__file__).ancestor(1)

TESTPYPI = "https://testpypi.python.org/pypi"


@task
def lint(ctx):
    """Run flake8 to lint code"""
    run("flake8")


@task
def freeze(ctx):
    """Freeze the pip requirements"""
    run("pip freeze -l > {req}".format(
        req=Path(ROOT_DIR, 'requirements.txt')))


@task(lint)
def test(ctx):
    """Lint and run unit tests"""
    cmd = "{} {} {}".format(
        "nosetests",
        "--with-coverage --cover-erase",
        "--cover-package=siganalysis --cover-html")
    run(cmd)


@task()
def release(ctx, deploy=False, test=False, version=''):
    """Tag release, run Travis-CI, and deploy to PyPI
    """
    if test:
        run("python setup.py check")
        run("python setup.py register sdist upload --dry-run")

    if deploy:
        run("python setup.py check")
        if version:
            run("git checkout master")
            run("git tag -a v{ver} -m 'v{ver}'".format(ver=version))
            run("git push")
            run("git push origin --tags")
            run("python setup.py register sdist upload")
    else:
        print("* Have you updated the version?")
        print("* Have you updated CHANGELOG.md?")
        print("* Have you fixed any last minute bugs?")
        print("If you answered yes to all of the above questions,")
        print("then run `invoke release --deploy -vX.YY.ZZ` to:")
        print("- Checkout master")
        print("- Tag the git release with provided vX.YY.ZZ version")
        print("- Push the master branch and tags to repo")
