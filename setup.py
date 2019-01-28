from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orvibo',

    version='1.5.0',

    description='Python module to controll Orvibo devices, such as s20 wifi sockets and AllOne IR blasters',
    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/cherezov/orvibo',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
)
