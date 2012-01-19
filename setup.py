#!env pyrhon

from distutils.command.build_py import build_py as _build_py
from distutils.core import setup

def test():
    """Specialized Python source builder."""

    from vector_dict import VectorDict
    from vector_dict.consistency import consistent_algebrae

    consistent_algebrae(
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
        version='0.1.0',
        author='Julien Tayon',
        author_email='julien@tayon.net',
        packages=['vector_dict'],
        url='http://gitbug.com/jul/ADDict_Addiction',
        license='LICENSE.txt',
        description='Implementing vector algebra on dict',
        long_description=open('README.rst').read(),
        requires=[
        "collections","math"
        ],
        classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: WTFPL',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
)
