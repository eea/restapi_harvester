#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click"]

setup_requirements = []

test_requirements = []

setup(
    author="Aitzol Naberan",
    author_email="anaberan@codesyntax.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="plone_restapi_harvester",
    name="plone_restapi_harvester",
    packages=find_packages(
        include=["plone_restapi_harvester", "plone_restapi_harvester.*"]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/aitzol/plone_restapi_harvester",
    version="0.1.0",
    zip_safe=False,
    entry_points={
        "console_scripts": ["harvester=plone_restapi_harvester.cli.cli:main"]
    },
)
