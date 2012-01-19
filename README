===========
Vector Dict
===========

Vector Dict provides all the expected operations on a dict as if it was
a vector. 

* a * vector (where a can be a scalar or a vector)
* vector1 + vector2 
* vector1 * vector2
* a / b (where at least one of a and b is a vector)
* cos(vector1,vector2) cosine similarity
* jaccard(vector1, vector2)

VectorDict is derived from defautdict thus it works the same for 
initialisation.

Properties being propagated to each level, it works on arbitrary depth dict

It provides some helpful helpers : 
path_from_array
as_vector_iter
as_row_iter


 

    #!/usr/bin/env python

    from vector_dict import VectorDict

    a = VectorDict( int, dict( x=1, y=1 ) )
    
    b = VectorDict( int, dict( x=1, y=0, z=0) )

    a + b  
    
    # Out : defaultdict(<type 'int'>, {'y': 1, 'x': 2, 'z' : 0 })
    
    a * b

    #Out : defaultdict(<class 'vector_dict.VectorDict'>, {'y': 0, 'x': 1})


    print a.cos(b) 

    # Out : 0.7071067811865475 
    
    # sqrt(2) / 2 = acos(45°)

    a.dot(b)

    # Out : 1.0 
    
    a.norm()

    # 1.4142135623730951

    a.pprint()
    
    # u'y'=1
    # u'x'=1



Helpers
=======

as_vector_iter
--------------

A generator of the vector in the form : 
path to key in the form of a set of keys , value (leaf)

    a = VectorDict( int, dict( a=1, b = VectorDict(int, dict(c=1)))) 
    
    [ (k, v) for  k,v in a.as_vector_iter() ]
    
    # Out: [(('a',), 1), (('b', 'c'), 1)]
 
as_row_iter
-----------
A generator of the vector as either tuple of ( (path), obj  ) or [ [ path +
obj ] ]
used for instance to ready a dict for a csv 
    
    a = VectorDict( int, dict( a=1, b = VectorDict(int, dict(c=1)))) 

    [ e for  e in a.as_row_iter(flatten=False) ]
    
    # Out : [(('a',), 1), (('b', 'c'), 1)]

    [ e for  e in a.as_row_iter(flatten=True) ]
    
    # Out : [['a', 1], ['b', 'c', 1]]


from_path_array
---------------

Build an intricated dict from an array representing a flat array of keys
ending by a value

    path_from_array( [ "a", "b" , 1 ])

    # Out : defaultdict(<class 'vector_dict.VectorDict'>, {'a': defaultdict(<class 'vector_dict.VectorDict'>, {'b': 1})})


Bibliography
============

`Cosine similarity and jaccard formula
<http://www.miislita.com/information-retrieval-tutorial/cosine-similarity-tutorial.html>`_ 

`Introduction to the use of vectors in data mining (in ruby)
<http://bionicspirit.com/blog/2012/01/16/cosine-similarity-euclidean-distance.html>`_ 
