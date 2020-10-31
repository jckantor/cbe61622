from setuptools import find_packages
from setuptools import setup

setup(
    name = 'cbelaboratory',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
)
