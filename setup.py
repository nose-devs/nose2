from setuptools import setup, find_packages

setup(
    name='nose2',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nose2 = nose2:main_',
            ],
        },
    include_package_data=True,
    package_data={'': ['nose2/plugins/plugins.cfg']},
)
