import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="deeptabular",
    version="0.0.1",
    author="Donald R. Williams",
    author_email="drwwilliams@ucdavis.edu",
    description="Spike and slab feature selection in Python",
    license="MIT",
    keywords="Bayesian",
    url="https://github.com/donaldRwilliams/spikeslab",
    packages=["spikeslab"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT Licence',
        'Operating System :: POSIX',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=[
        'pyjags',
        'numpy'
    ]
)