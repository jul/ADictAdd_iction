#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: yep
"""


from vector_dict.VectorDict import VectorDict, flattening, is_generator 
def find():
    """
    How to find all the sub dict in a tree that have the keys x, y, z at the same time time"""


    v = VectorDict( float, dict( x = 1, y = 1, z = 2 ) )
    w = VectorDict(float, dict( w = v, z = v ) )
    e = VectorDict(float, dict( a = w ) )
    print "%r" % [ el for el in e.find( 
            lambda k, v : 
                isinstance(v, dict) and set( ['x', 'y', 'z'] ) == set( v.keys() )
        ) ] 
    e.pprint()
find()
