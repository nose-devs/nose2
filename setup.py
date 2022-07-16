import os
import re

from setuptools import find_packages, setup


def read_version(filename):
    # use of " over ' will be enforced by "black"
    version_pattern = re.compile(r'__version__ = "([^"]*)"')
    with open(filename) as fp:
        for line in fp:
            m = version_pattern.match(line)
            if m:
                return m.group(1)
    raise Exception("could not parse version from {}".format(filename))


MAINTAINER = "Stephen Rosen"
MAINTAINER_EMAIL = "dev@nose2.io"

LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="nose2",
    version=read_version("nose2/__init__.py"),
    packages=find_packages(),
    extras_require={
        "coverage_plugin": ["coverage"],
        "dev": [
            "Sphinx",
            "sphinx_rtd_theme",
            "mock",
            "sphinx-issues",
        ],
    },
    entry_points={"console_scripts": ["nose2 = nose2:discover"]},
    # descriptive package info below
    description="unittest2 with plugins, the successor to nose",
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url="https://github.com/nose-devs/nose2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords=["unittest", "testing", "tests"],
)
