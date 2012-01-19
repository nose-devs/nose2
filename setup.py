import os
import sys

NAME = 'nose2'
VERSION = '0.1'
PACKAGES = ['nose2', 'nose2.plugins', 'nose2.plugins.loader',
            'nose2.tests', 'nose2.tests.functional', 'nose2.tests.unit']
SCRIPTS = ['bin/nose2']
DESCRIPTION = 'nose2 is the next generation of nicer testing for Python'
URL = 'https://github.com/nose-devs/nose2'
LONG_DESCRIPTION = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')).read()

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
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
)


py_version = sys.version[:3]

SCRIPT1 = 'nose2'
SCRIPT2 = 'nose2-%s' % (py_version,)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:

    REQS = ['six>=1.1,<1.2']
    if sys.version_info < (2, 7):
        REQS.extend(['unittest2>=0.5.1,<0.6', 'argparse>=1.2.1,<1.3'])

    params['entry_points'] = {
        'console_scripts': [
            '%s = nose2:main_' % SCRIPT1,
            '%s = nose2:main_' % SCRIPT2,
        ],
    }
    params['install_requires'] = REQS
    params['test_suite'] = 'nose2.compat.unittest.collector'

setup(**params)
