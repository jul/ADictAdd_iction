#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import Sequence, Mapping
from math import sqrt
#WTFPL
"""Overriding collections.DefaultDict to support addition """

all = ['VectorDict', 'objwalk', 'path_from_array', 'flattening', 'can_be_walked']
##mouais le test sur list ou tuple quand on a du numpy.array ça sux
## puis si on peut le parcourir ça quake "__iter__"


def path_from_array(path):
    """adding a path to a vector"""
    path_to_key = list(path)
    current = VectorDict( VectorDict, { path_to_key.pop() : path_to_key.pop()})
    while len(path_to_key):
        current = VectorDict( VectorDict, { path_to_key.pop() : current})
    return current 

def can_be_walked(stuff):
    """tells if it is walkable """
    return isinstance(stuff, list) or hasattr(stuff, "__iter__")


def flattening(a_duck):
    """flattening stuff // adapted from python cookbook"""
    if not can_be_walked(a_duck):
        yield a_duck
    else:
        for duckling in a_duck:
            if can_be_walked(duckling) and not isinstance( duckling, str) :
                for duck_eggs in flattening(duckling):
                    yield duck_eggs
            else:
                yield duckling



def objwalk(obj, path=(), limit=False, ):
    """
    Generator on all leaves of the object, return an array of the path and the
    leaf

    source:
     http://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    """
    if isinstance(obj, Mapping):
        for key, value in obj.iteritems():
            for child in objwalk(value, path + (key,)):
                yield child
    else:
        yield [x for x in flattening((path,  obj))]

def iter_object(obj, path=(), **opt):

    if isinstance(obj, Mapping):
        for key, value in obj.iteritems():
            for child in iter_object(value, path + (key,), **opt):
                yield  child
    else:
        yield  opt.get("flatten") and [ 
                x for x in flattening( ( path, obj) ) 
            ] or ( path, obj )

class VectorDict(defaultdict):
    """DefaultDict with addition"""

    def __init__(self, *a, **kw):
        """constructor"""
        defaultdict.__init__(self, *a, **kw)

    def __div__(left1, left2, *a, **lw):
        """dict by dict division"""
        if isinstance(left2, (float, int, complex)):
            return left1.__rdiv__(left2)
        if isinstance(left1, (float, int, complex)):
            return left2.__rdiv__(left1)
        else:
            return left1.divide(left2)
   


    def __mul__(left1, left2, *a, **lw):
        """muler"""
        if isinstance(left2, (float, int, complex)):
            return left1.__rmul__(left2)
        if isinstance(left1, (float, int, complex)):
            return left2.__rmul__(left1)
        else:
            return left1.homothetia(left2)

    def __neg__(self):
        for k, v in self.iteritems():
           self[k] = -1 * v
        return self

    
    def as_vector_iter(self, path=()): 
        """
        iterator on key value pair of nested dict in the form of 
        set( key0, key1, key2 ), child
        for a dict, therefore making a n-depth dict being homomorph
        to a single dimension vector in the form of 
        k , v 
        where k is the path, v is the leaf value
        source:
         http://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
        """
        return iter_object(self,(),flatten=False)
    
    def as_row_iter(self, path=(), **arg): 
        """
        iterator on key value pair of nested dict yielding items in the form
        set( key0, key1, key2 , child)
        very useful for turning a dict in a row for a csv output
        all keys and values are flattened
        """
        arg["flatten"] = arg.get("flatten", True)
        return iter_object(self,(),**arg )

    def divide(self, other):
        """multiplying to vectors as one vector of homothetia * vector
        it is a shortcut for a multiplication of a diagonal matrix
        missing keys in the pseudo diagonal matrix are pruned"""

        common_key =  set( self.keys() ) &  set( other.keys() )
        new_dict = VectorDict(VectorDict, dict() )
        for k in common_key:
            if  hasattr( self[k], "homothetia") :
                new_dict[k] = (self[k]).divide( other[k] )
            else:
                new_dict[k] = self[k] / other[k]
        return new_dict

    def homothetia(self, other):
        """multiplying to vectors as one vector of homothetia * vector
        it is a shortcut for a multiplication of a diagonal matrix
        missing keys in the pseudo diagonal matrix are pruned"""

        common_key =  set( self.keys() ) &  set( other.keys() )
        new_dict = VectorDict(VectorDict, dict() )
        for k in common_key:
            if  hasattr( self[k], "homothetia") :
                new_dict[k] = (self[k]).homothetia( other[k] )
            else:
                new_dict[k] = self[k] * other[k]
        return new_dict
    def dot(self, other):
        """scalar  = sum items self * other for each distinct key in common
        norm of the projection of self on other"""
        return sum( [ 1.0 * v for k,v in ( self * other ).as_vector_iter()  ] )
    
    #def values(self):
    #    return ( v for k,v in self.as_vector_iter() )

    def norm(self):
        """norm of a vector dict = sqrt( a . a  )"""
        return sqrt(self.dot(self))

    def cos( self, other ):
        """cosine similarity of two vector dicts
        a . b / ( ||a||*||b|| )
        """
        return 1.0 * self.dot( other) / self.norm() / other.norm()
    def jaccard(self, other):
        """jaccard similariry of two vectors dicts
        a . b  / ( ||a||^2 + ||b||^2 - a . b )
        """
        return 1.0 * self.dot(other) / (
            float( self.norm()) ** 2 +
            float( other.norm()) ** 2-
            self.dot(other) 
        )

            

    def __imul__(integer, self):
        if not isinstance(integer, int):
            raise Exception("wrong type in dict multiplication")
        #print "%r //%r" %  (self, integer)
        print "imul called"
        another = self.copy()
        #print "%r * %r " % (integer, another)
        for k, v in self.iteritems():
            another[k] = integer * v
        return another

    def __sub__(self, other):
        """subber"""
        positive = self.copy()
        negative = other
        neg_key = set(negative.keys())
        pos_key = set(positive.keys())
        for k, v in negative.iteritems():
            if k in positive.keys():
                positive[k] -= v
            else:
                positive[k] = -v
        return positive

    def __rdiv__(self, scalar):
        
        #print "%r //%r" %  (self, integer)
        another = self.copy()
        if isinstance(scalar, VectorDict ):
            return another.divide( scalar )
        #print "%r * %r " % (integer, another)
        for k, v in self.iteritems():
            another[k] =  v / scalar
        return another

    def __rmul__(self, scalar):
        #print "%r //%r" %  (self, integer)
        another = self.copy()
        if isinstance(scalar, VectorDict ):
            return self.homothetia(scalar)
            
        #print "%r * %r " % (integer, another)
        for k, v in self.iteritems():
            another[k] = scalar * v
        return another

    def __sub__(self, other):
        """subber"""
        positive = self.copy()
        negative = other
        neg_key = set(negative.keys())
        pos_key = set(positive.keys())
        for k, v in negative.iteritems():
            if k in positive.keys():
                positive[k] -= v
            else:
                positive[k] = -v
        return positive

    def pprint(self):
        print "\n".join( [ 
                    "%r=%r" % (
                        "->".join( map(unicode, k)), 
                        v
                    ) for k, v in self.as_vector_iter() ] )
                
    def __add__(left1, left2):
        """adder"""
        left1_big = len(left1.keys()) > len(left2.keys())
        bigger = left1_big and left1.copy() or left2.copy()
        smaller = left1_big and left2 or left1
        for k, v in smaller.iteritems():
            if k in bigger.keys():
                bigger[k] += v
            else:
                bigger[k] = v
        return bigger
        
    def __iadd__(self, other):
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

if '__main__' == __name__:
    print "undestranding 2 * array"
    from numpy import array, ndarray
   # def tracing(callme):
   #     def wrapper(callme):
   #         call_my_name = callme.__name__ or "oops"
   #         call_arg = "%r / %r" % (a, kw)
   #         print "IN: %r(%r)" % (call_my_name, call_arg)
   #         try:
   #             res = callme(*a, **kw)
   #         except Exception as e:
   #             print "OUT: E  %r" %  e
   #         print "OUT: %r => %r" % (callme, res)
   #         return result
   #     return wrapper
   # for method in VectorDict.__dict__.keys():
   #     if method.startswith("__"):
   #         print "%r " % (method,)
   #         setattr(int, method, tracing(method))

    print u"testing"

    a = VectorDict(VectorDict, {'FR': VectorDict(VectorDict,
        VectorDict(array, {'paris': array([1, 3])}))})

    print u"testing"
    a += VectorDict(
            VectorDict, {
                'FR': VectorDict(
                    VectorDict, VectorDict(
                            array, {'paris': array([1, 3])}
                       )
                   )
           }
       )
    b = VectorDict(
            VectorDict, {
                'FR':
                 VectorDict(VectorDict,
                        VectorDict(
                            array, {'lyon': array([1, 3])}
                       )
                    )
               }
          )
    print "%r" % a
    print "****%r" % b
    a += b
    for el in objwalk(a):
        print "<%r>" % (el or "",)
    print "%r" % "-".join( [ repr(k) for k,v in a.as_vector() ] )
