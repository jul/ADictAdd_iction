#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Clauses for common search on tree"""

import re
import types
class Clause(object):
    def __call__(self, value, *a , **kw):
        if self.__arg or self.__opt:
            real_clause = self.__clause(*self.__arg,**self.__opt) 
        else:
            real_clause = self.__clause
        return real_clause(value, *a, **kw)

    def __init__(self, functor, *a, **kw):
        self.__clause = functor
        self.__arg = a or None
        self.__opt = kw or None

find_re = Clause( lambda pattern : lambda v: not re.search(pattern,str(v)) is None ) 
"""Find if something match a regular expression"""

is_container = Clause(lambda v : isinstance(v, list) or hasattr(v, "__iter__"))
"""to know if something can contain more than one value (list , iterator, ...)"""

is_leaf = Clause(lambda v : not isinstance(v, dict))
"""is_leaf if value is not instance of dict"""

has_type = Clause(lambda _type : lambda v :  isinstance(v,_type))
"""Check if value has type _type"""

is_function = has_type( types.FunctionType )
"""check if value is a function"""

and_ = Clause( lambda v, *clauses:  all( [ clause(v) for clause in clauses ] ) )

has_all = Clause(
    lambda *k : lambda v : is_container(v) and all( map( lambda key: key in v, k))) 

or_ = Clause( lambda v, *clauses : any( [ clause(v) for clause in clauses ] )  )
not_ = Clause( lambda v, clause : not(clause(v) )  )

has_tree = Clause( lambda tree_clause: lambda v : ( not is_leaf(v) ) and v.match_tree(tree_clause)) 
"""Check if value has the subtree included in it"""

anything= Clause( lambda v : True )
"""matches anything"""


