#!/usr/bin/env python

import os
import sys
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#Include scaffolder
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'scaffolder')
    )
)

import scaffolder
scaffolder.install_minion_config('weaver')
#exit()

home = os.path.expanduser("~")
conf = os.path.join(home, ".minions", "weaver")


# if sys.argv[-1] == 'publish':
if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
# history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


test_requires = [
    'nose==1.3.0',
    'sure==1.2.2'
]
dev_requires = []

setup(
    name='scaffolder',
    version=scaffolder.get_version(),
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
        'console_scripts': [
            'scaffolder = scaffolder.cli:run',
        ]
    },
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    # dependency_links=parse_dependency_links('requirements.txt'),
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
