from setuptools import setup, find_packages

from packageinfo import VERSION, NAME, OSP_CORE_MIN, OSP_CORE_MAX

# Read description
with open('README.md', 'r') as readme:
    README_TEXT = readme.read()


# main setup configuration class
setup(
    name=NAME,
    version=VERSION,
    author='Author info',
    url='www.some_website.some_domain',
    description='The wrapper of something for SimPhoNy',
    keywords='simphony, cuds, something',
    long_description=README_TEXT,
    install_requires=[
        'osp-core>=' + OSP_CORE_MIN + ', <' + OSP_CORE_MAX,
    ],
    packages=find_packages(exclude=("examples", "tests")),
    test_suite='tests',
    entry_points={
        'wrappers':
            'wrapper = osp.wrappers.some_simulation_session:SomeSimulationSession'},
)
