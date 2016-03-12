from setuptools import setup, find_packages


setup(name='pkg1',
      packages=find_packages(),
      zip_safe=True,
      test_suite='nose2.collector.collector')
