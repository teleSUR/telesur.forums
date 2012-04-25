from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('docs/CREDITS.txt').read()
    + '\n' +
    open('docs/HISTORY.txt').read()
    + '\n')

setup(name='telesur.forums',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone :: 4.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Franco Pellegrini',
      author_email='frapell@ravvit.net',
      url='https://github.com/desarrollotv/telesur.forums',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['telesur'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.dexterity>=1.2.1',
          'plone.principalsource',
          'collective.prettydate',
          'borg.localrole',
          'plone.namedfile[blobs]',
          'plone.formwidget.captcha',
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
