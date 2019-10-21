from setuptools import setup, find_packages

from packageinfo import VERSION, NAME

# Read description
with open('README.md', 'r') as readme:
    README_TEXT = readme.read()


# main setup configuration class
setup(
    name=NAME,
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005)',
    url='www.simphony-project.eu',
    description='The wrappers sdk for SimPhoNy',
    keywords='simphony, cuds, Fraunhofer IWM, wrappers',
    long_description=README_TEXT,
    install_requires=[
        'simphony==2.0.1',
    ],
    packages=find_packages(),
)
