from setuptools import setup

setup(
    name='nose2',
    version='0.1',
    entry_points= {
        'console_scripts': [
            'nose2 = nose2:nose2_main',
            ],
        }
)
