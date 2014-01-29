#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# if sys.argv[-1] == 'publish':
if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
# history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'sh==1.08',
]
test_requires = []
dev_requires = []


setup(
    name='scaffolder',
    version='0.0.1',
    description='Simple terminal utility to scaffold projects from templates.',
    # long_description=readme + '\n\n' + history,
    long_description=readme + '\n\n',
    author='goliatone',
    author_email='hello@goliatone.com',
    url='http://github.com/goliatone/minions',
    packages=[
        'scaffolder'
    ],
    package_dir={'scaffolder': 'scaffolder'},
    entry_points={
        'console_scripts':[
            'scaffolder = scaffolder.main:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    keywords='',
    test_suite='test',
    extras_require={
        'test': test_requires,
        'develop': dev_requires,
    },
    license='MIT',
    classifiers=[

    ],
)