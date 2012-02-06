#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vector_dict.VectorDict import convert_tree
a = convert_tree( dict( a = 1, e = dict( b = dict( c= 1, d = True ) ), x= [ 1 , 2], z= 1.0  ))
### Traditionnal representation of a rooted tree made 
### when implemented with dict of dict
a.tprint()
# OUT: {
# OUT:     a = 1,
# OUT:     x = [1, 2],
# OUT:     z = 1.0,
# OUT:     e = {
# OUT:         b = {
# OUT:             c = 1,
# OUT:             d = True,
# OUT:         },
# OUT:     },
# OUT: }


### Flattening a tree as a vector
### which makes tree homeomorph to a vector
a.pprint()
# OUT: a = 1
# OUT: x = [1, 2]
# OUT: z = 1.0
# OUT: e->b->c = 1
# OUT: e->b->d = True

