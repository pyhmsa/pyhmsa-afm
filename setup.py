#!/usr/bin/env python

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

import versioneer

# Local modules.

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

setup(name='pyHMSA-afm',
      version=versioneer.get_version(),
      description='Interface between pyHMSA and AFM specific file formats',

      author='Philippe Pinard',
      author_email='philippe.pinard@gmail.com',

      url='http://pyhmsa.readthedocs.org',
      license='MIT',
      keywords='microscopy microanalysis hmsa file format user interface afm',

      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Physics',
        ],

      packages=find_packages(),

      install_requires=['pyHMSA', 'numpy'],
      tests_require=['nose', 'coverage'],

      zip_safe=False,

      test_suite='nose.collector',

      cmdclass=versioneer.get_cmdclass(),

      entry_points=\
         {'pyhmsa.fileformat.importer':
            ['AFM asc = pyhmsa_afm.fileformat.importer.asc:ImporterAFMAsc', ],
            },
     )
