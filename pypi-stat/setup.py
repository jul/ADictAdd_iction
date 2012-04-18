#!/usr/bin/env pyrhon
# -*- coding: "utf-8" -*-

from distutils.command.build_py import build_py as _build_py
from distutils.core import setup

#test()

setup(
        name='pypi-stat',
        version='0.5.0',
        author='Julien Tayon',
        author_email='julien@tayon.net',
        url= 'https://github.com/jul/ADictAdd_iction/tree/master/pypi-stat',
        packages=[],
        scripts = [ 'pypi_get_stat.py', 'pypi_graph_stat.py' ],
        license='LICENSE.txt',
        description='solution for getting packages stat, and graphing them',
        requires=['numpy', 'matplotlib','vector_dcit' ],
        classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
)
