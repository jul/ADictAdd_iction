#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import Sequence, Mapping
#WTFPL
"""Overriding collections.DefaultDict to support addition """

all = [ 'AccuDict', 'objwalk' , 'flattening' ]
##mouais le test sur list ou tuple quand on a du numpy.array ça sux
## puis si on peut le parcourir ça quake "__iter__"

def can_be_walked( stuff ):
    """tells if it is walkable """
    return isinstance( stuff,  list  ) or hasattr( stuff, "__iter__" )

def flattening( a_duck ):
    """flattening stuff // adapted from python cookbook"""
    if not can_be_walked( a_duck ):
        yield a_duck
    else:
        for duckling in a_duck:
            if can_be_walked( duckling ):
                for duck_eggs in flattening( duckling ) :
                    yield duck_eggs
            else:
                yield duckling

def objwalk(obj, path=(), limit = False ):
    """Generator on all leaves of the object, return an array of the path and the leaf
    # source http://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    """
    if isinstance(obj, Mapping):
        iterizer = hasattr( obj  , "iteritems" ) and obj.iteritems() or obj
        for key, value in iterizer:
            for child in objwalk(value, path + (key,)):
                yield child
    elif isinstance(obj, Sequence) and not isinstance(obj, basestring):
        for index, value in enumerate(obj):
            for child in objwalk(value, path + (index,)):
                yield child
    else:
        yield [ x for x in flattening( ( path , obj ) )  ]



class AccuDict(defaultdict):
    """DefaultDict with addition"""
    
    def __init__(self, *a, **kw) :
        """constructor"""
        defaultdict.__init__(self, *a, **kw )

    
    def __add__(left1, left2 ):
        """adder"""
        left1_big = len( left1.keys() )  > len( left2.keys() ) 
        bigger = left1_big and left1.copy() or left2.copy()
        smaller = left1_big and left2 or left1 
        for k, v in smaller.iteritems():
            if k in bigger.keys():
                bigger[k] += v 
            else:
                bigger[k] = v
        return bigger

    def __iadd__(self, other ):
        """adder"""
        self = self.__add__(other)
        return self
        #print "self %r" % self
        #print "other %r" % other
       
        #for k, v in other.iteritems():
        #    if k in self.keys():
        #        self[k] +=  v
        #    else:
        #        self[k] = v
        #print "self %r" % self

if '__main__' == __name__ :
    print u"testing"
    from numpy import array
    a = AccuDict( AccuDict, { 'FR' : AccuDict(AccuDict,  
        AccuDict( array, { 'paris' : array( [  1 , 3 ] )}  ) )} )

    print u"testing"
    a += AccuDict( 
            AccuDict, { 
                'FR' : AccuDict(
                    AccuDict, AccuDict( 
                            array, { 'paris' : array( [  1 , 3 ] )}  
                        ) 
                    )
            } 
        )
    b =  AccuDict( 
            AccuDict, { 
                'FR' : 
                 AccuDict( AccuDict,
                        AccuDict( 
                            array, { 'lyon' : array( [  1 , 3 ] ) }  
                        ) 
                     )
                } 
           ) 
    print "%r"  % a 
    print "****%r" % b
    a += b
    for el in objwalk( a ):
        print "<%r>" % ( el or "", )

