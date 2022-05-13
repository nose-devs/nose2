import os
import sys

from setuptools import find_packages, setup

VERSION = open("nose2/_version.py").readlines()[-1].split()[-1].strip("\"'")

MAINTAINER = "Stephen Rosen"
MAINTAINER_EMAIL = "dev@nose2.io"

PY_VERSION = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="nose2",
    version=VERSION,
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
    description="unittest2 with plugins, the succesor to nose",
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
