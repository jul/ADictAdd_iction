#!/usr/bin/env pyrhon
# -*- coding: "utf-8" -*-

from distutils.command.build_py import build_py as _build_py
from distutils.core import setup

def test():
    """Specialized Python source builder."""

    from vector_dict.VectorDict import VectorDict
    from  vector_dict.ConsistentAlgebrae import ConsistentAlgebrae

    ConsistentAlgebrae(
        context="test",
        neutral=VectorDict(int, {}),
        one=VectorDict(int, {"one": 1, "one_and_two": 3}),
        other=VectorDict(int, {"one_and_two": - 1, "two": 2}),
        another=VectorDict(int, {"one": 3, 'two':  2, "three": 1}),
        collect_values=lambda x: x.values()
        )

test()

setup(
        name='VectorDict',
        version='0.5.0',
        author='Julien Tayon',
        author_email='julien@tayon.net',
        packages=['vector_dict'],
        url='http://readthedocs.org/docs/vectordict/en/latest/',
        license='LICENSE.txt',
        test_suite='vector_dict.test.test_VectorDict',
        test='vector_dict.test.test_VectorDict',
        description='Implementing vector algebra on tree',
        requires=[
        "collections","math"
        ],
        classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
)
