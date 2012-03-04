#!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
"""test for rules of consistency in algebrae"""
#import os, sys, inspect
#cmd_folder = os.path.abspath(
#    os.path.join(
#        os.path.split(
#            inspect.getfile( inspect.currentframe() )
#        )[0] ,
#        ".."
#    )
#)
#if cmd_folder not in sys.path:
#   sys.path.insert(0, cmd_folder)



from vector_dict.VectorDict import VectorDict
from vector_dict.ConsistentAlgebrae import ConsistentAlgebrae

ConsistentAlgebrae(
    context="test",
    neutral=VectorDict(int, {}),
    one=VectorDict(int, {"one": 1, "one_and_two": 3}),
    other=VectorDict(int, {"one_and_two": - 1, "two": 2}),
    another=VectorDict(int, {"one": 3, 'two':  2, "three": 1}),
    collect_values=lambda x: x.values(),
    )


