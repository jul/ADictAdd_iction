#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""heritable traits of VectorDict 

 >>> from vector_dict.Operator import Adder,Subber
 >>> from collections import defaultdict
 >>> class dad(defaultdict,Adder,Subber):pass
 ... 
 >>> tata = dad( int, dict(a = 1, b = 0, c = -1 ) )
 >>> 
 >>> toto = dad( int, dict(a = 1 ) )
 >>> print toto+tata
 defaultdict(<type 'int'>, {'a': 2, 'c': -1, 'b': 0})
 >>> toto-=( tata+tata )
 >>> print toto
 defaultdict(<type 'int'>, {'a': -1, 'c': 2, 'b': 0})
"""

__all__ = [ 'Adder', 'Subber' ]
class Adder(object):
    def __add__(left1, left2):
        """adder"""
        left1_big = len(left1.keys()) > len(left2.keys())
        bigger = left1_big and left1.copy() or left2.copy()
        smaller = left1_big and left2 or left1
        bigger += smaller
        return bigger

    def __iadd__(self, other):
        for k,v in other.items() :
            self[k] = v+self[k] if k in self else v
        return self

class Subber(object):
    def __sub__(self, other):
        """subber"""
        positive = self.copy()
        negative = other
        positive -= negative
        return positive

    def __isub__(self, other):
        for k,v in other.iteritems() :
            self[k] = self[k]-v if k in self else -1*v
        return self


