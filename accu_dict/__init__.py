#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import Sequence, Mapping
#WTFPL
"""Overriding collections.DefaultDict to support addition """

all = [ 'AccuDict', 'objwalk' , 'flattening', 'can_be_walked' ]
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
        
        for key, value in obj.iteritems():
            for child in objwalk(value, path + (key,)):
                yield child
    elif isinstance(obj, Sequence) and not isinstance(obj, basestring):
        for index, value in enumerate(obj):
            for child in objwalk(value, path + (index,)):
                yield child
    else:
        yield [ x for x in flattening( ( path ,  obj  ) )  ]



class AccuDict(defaultdict):
    """DefaultDict with addition"""
    
    def __init__(self, *a, **kw) :
        """constructor"""
        defaultdict.__init__(self, *a, **kw )

    def __mul__(left1, left2, *a , **lw):
        """muler"""
        if isinstance( left2 , ( float, int, complex ) ):
            return left1.__rmul__( left2 )
        if isinstance( left1 , ( float, int, complex ) ):
            return left2.__rmul__( left1 )
        else:
            raise Exception("to be soon implemented")


    def __neg__(self):
        for k, v in self.iteritems():
            self[k] = -1 * v
        return self
        
    def __imul__( integer, self ):
        #print "%r //%r" %  ( self, integer ) 
        print "imul called"
        another = self.copy()
        #print "%r * %r " % ( integer, another ) 
        for k, v in self.iteritems():
            another[k] = integer * v
        return another
        
    def __sub__(self, other ):
        """subber"""
        positive = self.copy()
        negative = other
        neg_key = set( negative.keys() )
        pos_key = set( positive.keys() )
        for k, v in negative.iteritems():
            if k in positive.keys():
                positive[k] -= v 
            else:
                positive[k] = -v
        return positive

    def __rmul__(self, scalar ):
        #print "%r //%r" %  ( self, integer ) 
        another = self.copy()
        if not isinstance( scalar, ( float, complex, int ) ):
            raise Exception("Unhandled rmul type for %r " % scalar )
        #print "%r * %r " % ( integer, another ) 
        for k, v in self.iteritems():
            another[k] = scalar * v
        return another
        
    def __sub__(self, other ):
        """subber"""
        positive = self.copy()
        negative = other
        neg_key = set( negative.keys() )
        pos_key = set( positive.keys() )
        for k, v in negative.iteritems():
            if k in positive.keys():
                positive[k] -= v 
            else:
                positive[k] = -v
        return positive
   
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
    print "undestranding 2 * array"
    from numpy import array, ndarray
   # def tracing( callme):
   #     def wrapper( callme):
   #         call_my_name = callme.__name__ or "oops"
   #         call_arg = "%r / %r" % ( a , kw )
   #         print "IN : %r( %r )" % ( call_my_name, call_arg )
   #         try:
   #             res = callme( *a , **kw )
   #         except Exception as e :
   #             print "OUT: E  %r" %  e
   #         print "OUT : %r => %r" % ( callme, res)
   #         return result
   #     return wrapper
   # for method in AccuDict.__dict__.keys():
   #     if method.startswith("__"):
   #         print "%r " % ( method, ) 
   #         setattr( int , method, tracing(method) )




    
    print u"testing"
    
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

