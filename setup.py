from setuptools import setup

setup(
    # Application name:
    name='CPAPI',

    # Version number:
    version='0.2.0',

    # Application author details:
    author='Joshua Hatter',
    author_email='jhatter@themadhatter.org',

    # Packages
    packages=['cpapiweb'],

    # Details
    url='https://github.com/themadhatterz/cpapi',
    download_url = 'https://github.com/themadhatterz/cpapi/archive/v0.2.0.tar.gz',

    # License
    license='LICENSE.txt',
    description='Web interface for interacting with Check Point Software Management API.',

    # Dependent packages
    install_requires=[
        'flask',
        'flask_nav',
        'requests>=2.18.4',
        'urllib3>=1.22'
    ],
)
