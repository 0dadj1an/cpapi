from distutils.core import setup

setup(
    # Application name:
    name='CPAPI',

    # Version number (initial):
    version='0.1.0',

    # Application author details:
    author='Joshua Hatter',
    author_email='jhatter@themadhatter.org',

    # Packages
    packages=['cpapiweb'],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url='https://github.com/themadhatterz/cpapi',

    # License
    license='LICENSE.txt',
    description='Web interface for interacting with Check Point Software Management API.',

    long_description='README.md',

    # Dependent packages (distributions)
    install_requires=[
        'flask',
        'flask_nav'
        'requests',
    ],
)
