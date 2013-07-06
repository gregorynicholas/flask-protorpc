#!/usr/bin/env python
"""
flask_protorpc
--------------

An extremely thin Flask Extension to build remote clients.

`````

"""
from setuptools import setup

with open("requirements.txt", "r") as f:
  requires = f.readlines()

with open("README.md", "r") as f:
  long_description = f.read()


setup(
  name='flask-protorpc',
  version='1.0.0',
  url='http://github.com/gregorynicholas/flask-protorpc',
  license='MIT',
  author='gregorynicholas',
  author_email='gn@gregorynicholas.com',
  description=__doc__,
  long_description=long_description,
  py_modules=[
    'flask_protorpc',
    'flask_protorpc_tests',
    'testutils',
  ],
  zip_safe=False,
  platforms='any',
  install_requires=requires,
  dependency_links=[
    'https://github.com/gregorynicholas/google-protorpc/tarball/master',
  ],
  test_suite='flask_protorpc_tests',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
