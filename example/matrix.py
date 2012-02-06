#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Matrix of VectorDict"""
import os, sys, inspect
cmd_folder = os.path.abspath(
    os.path.join(
        os.path.split(
            inspect.getfile( inspect.currentframe() )
        )[0] ,
        ".."
    )
)
if cmd_folder not in sys.path:
   sys.path.insert(0, cmd_folder)





from vector_dict.Clause import Clause, is_leaf, is_container

from vector_dict.Operation import  identity, mul, cast
from vector_dict.VectorDict import convert_tree
from vector_dict.SparseMatrix import SparseMatrix,Coordinates
from collections import namedtuple, defaultdict

a = convert_tree( { 'a' : { 'b' : 1 , 'c' : 2 } , 'b' : 0 } )

def title(string):
    print 
    print "*" * 80
    print string
    print "*" * 80
title( "initial dictionary" )
a.tprint()

m = SparseMatrix( 
    ## take source['a'][b'] and * -2 and put it in dst['mul']['neg2']
    ( tuple( [ 'a', 'b' ] ), tuple([ 'mul', 'neg2' ] ), mul(-2) ),
    ## guess :) 
    ( tuple([ 'a', 'c' ]), tuple([ 'mul', 'misplaced' ]), cast(float) ),
    ( tuple([ 'b' ])  , tuple([ 'a' ]) , lambda x : -4 ),
    ( tuple( [ 'a' ] ), tuple( [ 'a_dict' ] ), identity ),
    )
title( "transformed dict" )
m(a).tprint()
w = SparseMatrix()
w[ 
    Coordinates( src= tuple( [ ] ) , 
    dst =  tuple([ 'a_copy' ] ))
]=  identity 
w[ 
    Coordinates( src= tuple( [ ] ) , 
    dst =  tuple([ 'inception' ] ))
]=  m.copy()  

title( "with matrix in matrix" )
w(a).tprint()

"""
********************************************************************************
initial dictionary
********************************************************************************
{
    a = {
        c = 2,
        b = 1,
    },
    b = 0,
}

********************************************************************************
transformed dict
********************************************************************************
{
    a = -4,
    mul = {
        neg2 = -2,
    },
    a_dict = {
        c = 2,
        b = 1,
    },
}

********************************************************************************
with matrix in matrix
********************************************************************************
{
    inception = {
        a = -4,
        mul = {
            neg2 = -2,
        },
        a_dict = {
            c = 2,
            b = 1,
        },
    },
    a_copy = {
        a = {
            c = 2,
            b = 1,
        },
        b = 0,
    },
}
"""
