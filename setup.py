import os
import sys

from setuptools import setup

VERSION = open("nose2/_version.py").readlines()[-1].split()[-1].strip("\"'")

# TODO: potentially change author?
AUTHOR = "Jason Pellerin"
AUTHOR_EMAIL = "jpellerin+nose@gmail.com"

py_version = sys.version_info


LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="nose2",
    version=VERSION,
    packages=[
        "nose2",
        "nose2.plugins",
        "nose2.plugins.loader",
        "nose2.tests",
        "nose2.tests.functional",
        "nose2.tests.unit",
        "nose2.tools",
    ],
    install_requires=[
        "six>=1.7",
        "coverage>=4.4.1",
        # mock on py2, py3.4 and py3.5
        # not just py2: py3 versions of mock don't all have the same
        # interface and this can cause issues
        'mock==2.0.0;python_version<"3.6"',
    ],
    extras_require={
        "coverage_plugin": ["coverage>=4.4.1"],
        "doc": ["Sphinx>=1.6.5", "sphinx_rtd_theme", "mock"],
    },
    entry_points={
        "console_scripts": [
            "nose2 = nose2:discover",
            "nose2-%s.%s = nose2:discover" % (py_version.major, py_version.minor),
        ]
    },
    test_suite="unittest.collector",
    # descriptive package info below
    description="unittest2 with plugins, the succesor to nose",
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://github.com/nose-devs/nose2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords=["unittest", "testing", "tests"],
)
