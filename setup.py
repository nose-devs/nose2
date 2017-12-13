import os
import sys

from os.path import dirname

NAME = 'nose2'
VERSION = open('nose2/_version.py').readlines()[-1].split()[-1].strip('"\'')
PACKAGES = ['nose2', 'nose2.plugins', 'nose2.plugins.loader',
            'nose2.tests', 'nose2.tests.functional', 'nose2.tests.unit',
            'nose2.tools']
SCRIPTS = ['bin/nose2']
DESCRIPTION = 'nose2 is the next generation of nicer testing for Python'
URL = 'https://github.com/nose-devs/nose2'
LONG_DESCRIPTION = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')).read()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Testing',
]

AUTHOR = 'Jason Pellerin'
AUTHOR_EMAIL = 'jpellerin+nose@gmail.com'
KEYWORDS = ['unittest', 'testing', 'tests']

params = dict(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=PACKAGES,
    scripts=SCRIPTS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    extras_require={
        'coverage_plugin': ["coverage>=4.4.1"],
    }
)


py_version = sys.version_info

SCRIPT1 = 'nose2'
SCRIPT2 = 'nose2-%s.%s' % (py_version.major, py_version.minor)


def parse_requirements(requirement_file):
    requirements = []
    with open(requirement_file) as file_pointer:
        for line in file_pointer:
            if line.strip() and not line.strip().startswith('#'):
                requirements.append(line.strip())
    return requirements


def add_per_version_requirements():
    extra_requires_dict = {}
    for current_file in os.listdir(dirname(__file__) or '.'):  # the '.' allows tox to be run locally
        if not current_file.startswith('requirements-') or 'docs' in current_file:
            continue
        python_version = current_file[len('requirements-'):-len('.txt')]
        extra_requires_key = ':python_version == "{}"'.format(python_version)
        extra_requires_dict[extra_requires_key] = parse_requirements(current_file)
    return extra_requires_dict

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:

    params['entry_points'] = {
        'console_scripts': [
            '%s = nose2:discover' % SCRIPT1,
            '%s = nose2:discover' % SCRIPT2,
        ],
    }
    params['install_requires'] = parse_requirements('requirements.txt')
    params['test_suite'] = 'unittest.collector'
    params['extras_require']['doc'] = parse_requirements('requirements-docs.txt')
    params['extras_require'].update(add_per_version_requirements())

setup(**params)
