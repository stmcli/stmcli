# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stmcli',
    version='1.2.1',
    description='The unofficial STM CLI client.',
    long_description=long_description,
    url='https://github.com/stmcli/stmcli',
    author='Pascal Boardman / Philippe Dagenais',
    author_email='pascalboardman@gmail.com',
    license='MIT',
    scripts=['bin/stmcli'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='stm montreal autobus bus schedule horaire',
    packages=['stmcli'],
    install_requires=['peewee', 'unicodecsv', 'xmltodict'],
)
