from vector_dict.VectorDict import VectorDict, convert_tree, is_leaf
from vector_dict.Clause import *
def findme( v, a_tree):
    if not is_leaf(v): 
        return v.match_tree(a_tree)

positive = lambda v : v > 0

def pretty_present(list):
    print "Result "
    for el in list:
        print "path %r " % el[0]
        print "has value %s" %  (hasattr(el[1], 'tformat') and el[1].tformat() or el[1] )

    print
w = convert_tree( dict( 
    a = dict( c=  1),
    e = dict( d= 3.0) ,
    b = dict( c = 1 , d = 4 )
))

w.tprint()

pretty_present( w.find( lambda p, v : has_all( 'c', 'd' )(v) ) )

pretty_present( w.find( lambda p, v : findme(v, dict( 
                                        d= has_type(int), 
                                        c=has_type(int)   )
) ) ) 

pretty_present( w.find( lambda p, v : has_tree({  'a' : { 'c' : positive  } })(v)) )

pretty_present( w.find( lambda p, v : ( 
        has_type( int )(v) or has_type(float)(v)
    ) and  v > 3  ))
pretty_present( w.find( lambda p, v : p.endswith( [ 'c' ] ) ) )


"""
RESULTS : 
{
    a = {
        c = 1,
    },
    b = {
        c = 1,
        d = 4,
    },
    e = {
        d = 3.0,
    },
}
Result 
path ['b'] 
has value {
    c = 1,
    d = 4,
}

Result 
path ['b'] 
has value {
    c = 1,
    d = 4,
}

Result 
path [] 
has value {
    a = {
        c = 1,
    },
    b = {
        c = 1,
        d = 4,
    },
    e = {
        d = 3.0,
    },
}

Result 
path ['b', 'd'] 
has value 4

Result 
path ['a', 'c'] 
has value 1
path ['b', 'c'] 
has value 1
"""
