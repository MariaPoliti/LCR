import os

import setuptools
from setuptools import setup

setup(name='LCR',
      description='package to operate an Agilent/Keysight A4980E LCR meter \
                    using python',
      description_content_type='text/markdown; \
                                charset=UTF-8; variant=GFM',
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown; \
                                     charset=UTF-8; variant=GFM',
      url='https://github.com/EISy-as-Py/hardy',
      license='MIT',
      author='Maria Polit',
      python_requires="~=3.5",

      packages=setuptools.find_packages())

classifiers = ("Programming Language :: Python :: 3",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent")
