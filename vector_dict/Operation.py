#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""misc function that can be used on tree or leaf
just for convenience

identity : 
    return itself

copy : 
    return a copy of a value

mul(by) : 
    return a function that multiples by a value

cast(type) : 
    cast the element in given type
"""

identity = lambda x : x 
copy = lambda x : x.copy()
mul = lambda by :  lambda x : x * by 
cast = lambda _type : lambda x : _type(x)
