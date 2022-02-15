"""Installation script for your wrapper.

This script is designed to work with setuptools. It defines the metadata and
the files to be included in the Python package of your wrapper.

We strongly encourage you to read the "Packaging Python Projects" tutorial,
https://packaging.python.org/en/latest/tutorials/packaging-projects/ that
gives a detailed description on how to write this file. Here only provide a
minimalistic (although functioning) version.
"""

from setuptools import find_packages, setup

from packageinfo import NAME, OSP_CORE_MIN, OSP_CORE_MAX, VERSION

# Read description
with open('README.md', 'r', encoding="utf8") as readme:
    README_TEXT = readme.read()


# Setup configuration class instantiation. Here is where the metadata of
# your package is fixed.
setup(
    name=NAME,
    version=VERSION,
    author='Author info',
    url='https://www.your_website.domain',
    description='Mytool wrapper for SimPhoNy',
    keywords='simphony cuds yourkeyword',
    long_description=README_TEXT,
    install_requires=[
        f'osp-core >= {OSP_CORE_MIN}, < {OSP_CORE_MAX}'
    ],
    packages=find_packages(
        exclude=("examples",
                 "tests")),
    entry_points={
        'wrappers':
            'wrapper = osp.wrappers.'
            'your_wrapper_sessionsession:YourWrapperSession'},
)
