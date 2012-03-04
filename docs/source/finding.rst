Accessing, selecting and modifying elements in a tree
=====================================================


For convenience purpose, the result of the find method returns a namedtuple
Element where 

* Element[0] is the same as Element.path : the path to the value,
* Element[1] is the same as Element.value : the value


predicates on path
******************

As path is of the Path class, you can use *endswith*, *startswith* and *countains* methods. 


 >>> from vector_dict.VectorDict import convert_tree, VectorDict
 >>> a = convert_tree( { 'a' : { 'a' : { 'r' : "yop" , 'b' : { 'c' :  1 }, 'd' : True } } } )
 >>> a.pprint()
 a->a->r = 'yop'
 a->a->b->c = 1
 a->a->d = True
 >>> a.tprint()
 {
     a : {
         a : {
             r : 'yop',
             b : {
                 c : 1,
             },
             d : True,
         },
     },
 }
 >>> print "\n".join([ 
        "%r => %r"  %( e.path, e.value ) for e in a.find( 
            lambda k, v : k.endswith( 'a','r' ) )
    ])
  ('a', 'a', 'r') => 'yop'
  
If you ask a condition on path only, it will return **all** nodes verifying the condition 

**code continued from first example**
 
 >>> a.build_path( "a", "a", "g", "a", 2 )
 >>> [ e.path for e in a.find( lambda k,v : k.contains( 'a' ) ) ]
 [('a',), ('a', 'a'), ('a', 'a', 'r'), ('a', 'a', 'b'), ('a', 'a', 'b', 'c'), ('a', 'a', 'd'), ('a', 'a', 'g'), ('a', 'a', 'g', 'a')]

Limiting the matching elements to leaves
****************************************

If you dont want any answers returned in the form of a tree add the is_leaf clause :

**code continued from first example**

 >>> from vector_dict.Clause import is_leaf        
 >>> [ e.path for e in a.find( lambda k,v : k.contains( 'a' )  and is_leaf(v)) ]
 [('a', 'a', 'r'), ('a', 'a', 'b', 'c'), ('a', 'a', 'd'), ('a', 'a', 'g', 'a')]
 >>> [ e.value for e in a.find( lambda k,v : k.contains( 'a' )  and is_leaf(v)) ]
 ['yop', 1, True, 2]
 >>> [ e for e in a.find( lambda k,v : k.contains( 'a' )  and is_leaf(v)) ]
 [Element(path=('a', 'a', 'r'), value='yop'), Element(path=('a', 'a', 'b', 'c'), value=1), Element(path=('a', 'a', 'd'), value=True), Element(path=('a', 'a', 'g', 'a'), value=2)]
 >>> a.tprint()
 {
     a : {
         a : {
             r : 'yop',
             b : {
                 c : 1,
             },
             d : True,
             g : {
                 a : 2,
             },
         },
     },
 }
       
Searching a specified location of a tree
****************************************

You can also narrow your search on a subtree with the given path by combining with at() method. For instance searching in 'a' and 'b' subtree

 >>> from vector_dict.VectorDict import convert_tree, VectorDict,Element,Path
 >>> a = convert_tree(dict(a=dict(x=1, y=2, z=3), b=dict( x=-1, y=-1, z = -2)))
 >>> [ e for e in a.at( 'b' ).find( lambda k, v : k.endswith('x')) ]
 [Element(path=('x',), value=-1)]
 >>> [ e for e in a.at( 'a' ).find( lambda k, v : k.endswith('x')) ]
 [Element(path=('x',), value=1)]

Mainpulating values yielded by the find method
**********************************************

Also with at you can manipulate values : 

**code continued from the above example**

 >>> [ a.at(e.path , lambda v : v * -10 ) for e in a.find( lambda k, v : k.endswith('x')) ]
 [-10, 10]
 >>> a.tprint()
 {
     a : {
         y : 2,
         x : -10,
         z : 3,
     },
     b : {
         y : -1,
         x : 10,
         z : -2,
     },
 }

.. warning::
    * Since it is pretty not a good idea to change a collection while it is being iterated any in situ search / replace at the same time is strongly discouraged;
    * Always work with the path when manipulating








