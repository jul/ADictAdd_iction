#!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
"""test for rules of consistency in algebrae"""

import sys
import os
from os import path

base_dir = os.path.dirname(__file__) or '.'
sys.path += [ path.abspath( path.join(base_dir, "..") ) ]
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


