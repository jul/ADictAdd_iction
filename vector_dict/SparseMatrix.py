#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Dict behaving like a vector, and supporting all operations
the algebraic way
"""
import types
from Clause import Clause, is_leaf, is_container

from VectorDict import VectorDict, Path, tree_from_path
from collections import namedtuple, defaultdict
#WTFPL

__all__ = [ 'Coordinates', 'SparseMatrix' ]


## bug in build path
## temporaly using add_path

Coordinates = namedtuple("Coordinates", "src, dst")
class SparseMatrix(VectorDict):
    """Sparse Matrice on dict of dict of dict
    a sparse matrix is a set of 
        - src path coordinate
        - dst path coordinate
        - and a fonction to apply on the src value 
        to transform it in destination value
   """

    def __init__(self, *coord_fonc, **kw  ):
        if coord_fonc and isinstance(  coord_fonc[0], types.TypeType) :
            super( VectorDict, self).__init__( *coord_fonc, **kw)
        else:
            super( VectorDict, self).__init__(  VectorDict, {} )
            for src, dst, funct in ( a_set  for a_set in coord_fonc):
                coord = Coordinates( src = src, dst = dst )
                self[coord] = funct

#    def copy(self):
#        return super( defaultdict, self).copy()

    def __call__(self, src):
        dst = VectorDict(VectorDict, {} )
        for coord, funct in self.iteritems():
            if not is_leaf(funct):
                real_func = lambda v : funct(v)
            else:
                real_func = funct
            
            dst.build_path(   
                *( list(coord.dst) + [ real_func( src.at( coord.src) ) ]) 
            )
        return dst

if '__main__' == __name__: 
    from VectorDict import convert_tree
    from Operation import  identity, mul, cast
    a = convert_tree( { 'a' : { 'b' : 1 , 'c' : 2 } , 'b' : 0 } )
    a.pprint()
    print a.at( [ 'a', 'c' ]  )
    m = SparseMatrix( 
        ( tuple( [ 'a', 'b' ] ), tuple([ 'mul', 'neg2' ] ), mul(-2) ),
        ( tuple([ 'a', 'c' ]), tuple([ 'mul', 'misplaced' ]), cast(float) ),
        ( tuple([ 'b' ])  , tuple([ 'a' ]) , lambda x : -4 ),
        ( tuple( [ 'a' ] ), tuple( [ 'a_dict' ] ), identity ),
        )
    m.pprint()
    print "**************"
    print m(a)
    m(a).pprint()
    print "iiiiiiiiiiiiiiiiiiiiiiiiiiiii" 
    w = SparseMatrix()
    w[ 
        Coordinates( src= tuple( [ ] ) , 
        dst =  tuple([ 'a_copy' ] ))
    ]=  identity 
    w[ 
        Coordinates( src= tuple( [ ] ) , 
        dst =  tuple([ 'inception' ] ))
    ]=  m.copy()  
   
    w(a).pprint()
