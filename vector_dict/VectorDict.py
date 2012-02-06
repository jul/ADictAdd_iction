#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dict behaving like a vector, and supporting all operations
the algebraic way
"""
from collections import defaultdict
from collections import Sequence, Mapping
from math import sqrt
import types
from  Clause import Clause, is_leaf, is_container, is_function
#WTFPL

__all__ = ['cos', 'dot',  'iter_object' , 'tree_from_path', 'Path',
    'flattening', 'can_be_walked']


def convert_tree(a_tree):
    """
    convert from any other nested object to a VectorDict 
    works very well with nested dict
    Dont work as a method (why ?)
    """
    a_vector_dict = VectorDict()

    for e in iter_object_nl(a_tree, flatten = True):
        a_vector_dict += tree_from_path( e )
    return a_vector_dict

class Path(  list):
    def endswith( self, a_tuple ):
        return self[len(self) - len(a_tuple) : ] == a_tuple

    def startswith( self, a_tuple ):
        return self[: len( a_tuple ) ] == a_tuple

    def contains( self, a_tuple, _from = 0, follow = 0):
        if len( a_tuple) == follow:
            return True
        index = False
        try:
            here = self[ _from:]
            if len(here ) < len(a_tuple[follow:]):
                return False
        except IndexError:
            return False

        try:
            index = here.index(a_tuple[follow] )
            return  self.contains(
                    a_tuple, 
                        index +  1 , 
                        follow + 1
                    )
        except ValueError:
            return False
        except IndexError:
            return self.contains(a_tuple, _from +  1 )
        return False

def dot( obj1, obj2):
    """for ease of reading and writing"""
    return obj1.dot(obj2)

def cos( obj1, obj2):
    """for ease of reading and writing"""
    return obj1.cos(obj2)



def tree_from_path(path):
    """adding a path to a vector"""
    path_to_key = list(path)
    root = VectorDict( VectorDict, { path_to_key.pop() : path_to_key.pop()})
    current = root
    while len(path_to_key):
        current = VectorDict( VectorDict, { path_to_key.pop() : current})
    return current

def can_be_walked(stuff):
    """tells if it is walkable """
    return isinstance(stuff, list) or hasattr(stuff, "__iter__")

def is_generator(stuff):
    """tells if it is a generator"""
    return isinstance(stuff, types.GeneratorType)

def flattening(a_duck, taxonomy = can_be_walked ):
    """flattening stuff // adapted from python cookbook"""
    if not taxonomy(a_duck):
        yield a_duck
    else:
        for duckling in a_duck:
            if taxonomy(duckling) and not isinstance( duckling, str) :
                for duck_eggs in flattening(duckling, taxonomy = taxonomy):
                    yield duck_eggs
            else:
                yield duckling



def iter_object_nl(obj, path=(), **opt):
    """
    Generator on all leaves of the object, return an array of the path and the
    leaf

    source:
     http://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    """

    if isinstance(obj, Mapping):
        for key, value in obj.iteritems():
            for child in iter_object_nl(value, path + (key,), **opt):
                yield  child
    else:
        yield  opt.get("flatten") and  [
                x for x in flattening(  path)  
            ] + [   obj ]  or ( path, obj )

def iter_object(obj, path=(), **opt):
    """
    Generator on all leaves of the object, return an array of the path and the
    leaf

    source:
     http://tech.blog.aknin.name/2011/12/11/walking-python-objects-recursively/
    """

    if isinstance(obj, Mapping):
        for key, value in obj.iteritems():
            for child in iter_object(value, path + (key,), **opt):
                yield  child
    else:
        yield  opt.get("flatten") and [ 
                x for x in flattening( ( path, obj) ) 
            ] or ( path, obj )

class VectorDict(defaultdict):
    """Dict that supports all operations the way of vector does : 
    + - / * dot, and operations with scalars"""
    def __init__(self, *a , **a_dict ):
        
        super( VectorDict, self).__init__( *a,**a_dict)

    def from_tree( self, a_tree):
        """Create a VectorDict Intrication from a tree
        Drawback there is no factory specified
        """
        self =  convert_tree( a_tree)

    def match_tree(self, a_tree):
        """does the tree given ha an argument match the actual 
        tree.
        if tree leaves are Clauses, the match_tree will apply 
        the clauses.
        """
        match_to_find = len(a_tree.keys())
        if not set(a_tree).issubset( set(self.keys())):
            return False
        for k,v in a_tree.iteritems():
            if k in self:
                if is_leaf(v):
                #terminaison of the comparison tree
                    if isinstance(
                            v, Clause
                        ) or isinstance( 
                            v , types.FunctionType
                        ):
                    # if it is a clause apply it to the targeted tree
                        match_to_find -= v(self.get(k)) and 1 or 0
                    else:
                    ## it is not a clause
                        val = self.get(k)
                        if  is_leaf(val):
                        ## terminating values match
                            match_to_find -= v ==  val and 1 or 0
                        else:
                        ## the compared tree goes on, we match the keys
                            match_to_find -=  v in val  and 1 or 0
                else:
                    ## the comparison tree goes on
                    sub_tree = self.get(k)
                    if not is_leaf(sub_tree):
                        ## the compared tree goes on 
                        ## we recurse
                        match_to_find -= sub_tree.match_tree( v ) and 1 or 0
                    else:
                        ### the compared tree is smaller than the comparison 
                        ## tree
                        match_to_find -= v ==sub_tree and 1 or 0 
                        #return False
        return 0 == match_to_find

    def add_path(self, path):
        """ same as buildpath other implementation, 
        I need to make test, this one seems less interesting"""
        self += tree_from_path( path)
        self.__setitem__(path[0],self[path[0]])
        ### fighting against amnesia


    def build_path( self, *path):
        """ implementation of constructing a path in a tree, argument is 
        a serie of key """
        if len(path) == 2:
            key, value = path[0:2]
            if  key in self.keys() or self.get(key):
                raise ValueError( "collision of values")
            self.__setitem__( key, value )
        if len(path) > 2:
            key, value = path[0:2]
            if key in self.keys() and self.get(key):
                if  value in self[key].keys():
                    self[key].build_path( path[1:])
            else:
                if key in self.keys():
                    raise Exception("Path already present")
            self.__setitem__( key,  tree_from_path( path[1:] ))

    def prune(self, *path):
        """delete all items at path """
        todel = None
        if len(path)>1:
            self.at(path[:-1]).__delitem__(path[-1])
        else:
            self.__delitem__( path[0] )

    def push(self, path, value ):
        """ pushing value at place given by path
        will create the path if inexistent"""
        self.build_path( path + [ v ] )

    def get_at(self, *path):
        """ get element at path given has a serie of key"""
        return self.at( path, None , True)

    def at(self, path, apply_here = None, copy = False):
        """
        gets to the mentioned path eventually apply a lambda on the value
        and return the node, 
        and copy it if mentioned. 
        
        """
        here = self
        if apply_here and not( is_function(apply_here) ):
            raise Exception("second argument must be a function to apply on path")
        if not len(path):
            if apply_here:
                raise Exception("cant apply a function on root of %r" % self)
            if copy:
                return  self.copy() 
            return   self
        for e in path[:-1]:
            if not hasattr(here, "__getitem__"):
                raise IndexError("this path dont exists")
            if not here.__getitem__(e):
                raise Exception("Path %r does not exists in the tree" %path ) 
            here = here.__getitem__(e)
        if not apply_here is None:
            here.__setitem__(path[-1],apply_here(here[path[-1]]))
        value = here[path[ -1 ] ]

        if copy and is_container(value):
            return here[path[-1]].copy()
        return value


    def __flatten_generator(func):
        def wrap(*a, **kw):
            return flattening( func( *a, **kw ), taxonomy = is_generator ) 
        wrap.__doc__ = func.__doc__
        return wrap

    #@flatten_generator
    def diff(self, other, diff_mine = None,diff_other=None, path = []):
        def prune( key, adict):
            def todo():
                adict.__delitem__(key)
            return [ todo ]

        def cp_if_dict(val):
            return isinstance( v, dict) and v.copy() or v
        if not diff_mine:
            diff_mine = VectorDict( VectorDict, {} )
            diff_other = VectorDict( VectorDict, {} )
        for k, v in self.iteritems():
            if not k  in other.keys():
            ## pour que l'autre me ressemble enlevons toutes les clés
                diff_other += tree_from_path(  path + [k, prune( k, self)  ] )
            else:
                ## k in other.keys()
                ## les clés sont dans les deux arbres
                if v != other[k] :
                    if isinstance( v , VectorDict) and isinstance( 
                        other[k], VectorDict):
                        vd_m, vd_o = v.diff(  other[k],  diff_mine, diff_other,  path + [ k ] )
                        diff_mine = diff_mine + vd_m
                        diff_other = diff_other + vd_o
                    elif isinstance( v , VectorDict) or isinstance( 
                        other[k], VectorDict):
                        diff_mine +=  tree_from_path(  path + [k, cp_if_dict( other[k]) ] )
                    else: 
                        diff_mine +=  tree_from_path( path + [k, - other[k]    ] )

                
                else:
                    if isinstance( v, VectorDict ):
                        vd_m, vd_o = v.diff(  other[k],  diff_mine, diff_other,  path + [ k ] )
                        diff_mine = diff_mine + vd_m
                        diff_other = diff_other + vd_o
                    
        for k , v in other.iteritems():
            if not k  in self.keys():
                diff_mine += tree_from_path( path + [k, v ] )

        return diff_mine, diff_other
               


    def __div__(left1, left2, *a, **lw):
        """dict by dict division"""
        if isinstance(left2, (float, int, complex)):
            return left1.__rdiv__(left2)
        if isinstance(left1, (float, int, complex)):
            return left2.__rdiv__(left1)
        else:
            return left1.divide(left2)
   
    @__flatten_generator
    def find(self, predicate_on_path_value, path = [] ):
        """apply a fonction on value if predicate on key is found"""
        path = Path( path + [] )
        if predicate_on_path_value(Path( path) , self):
            yield  Path( path + [] )  ,self
        for k,v in self.iteritems():
            if isinstance(v, VectorDict ):
                yield    v.find( predicate_on_path_value, Path( path + [ k ] ) )
            else:
                if predicate_on_path_value(Path( path + [k]), v):
                    yield  Path( path + [k])  ,v 

                 

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

    def tformat(self, indent_level = 0, base_indent = 4):
        """pretty printing in a tree like form à la Perl"""
        offset = " " *  indent_level * base_indent
        toreturn = '{\n'
        for k,v in self.iteritems():
            toreturn += offset + ( " " * base_indent ) +  '%s = ' % k
            if hasattr( v, "tformat"):
                toreturn += v.tformat( indent_level+1, base_indent )
            else:
                toreturn += "%s" % ( isinstance( v, ( str, unicode) ) and ( "'%s'" % v ) or repr(v) )
            toreturn += ',\n'
        toreturn += offset +  '}'
        return toreturn 

    def tprint( self, indent_level = 0, base_indent = 4):
        print self.tformat( indent_level, base_indent )
 
    def pprint(self):
        """ pretty printing the VectorDict in flattened vectorish representation"""
        print "\n".join( [ 
                    "%s = %s" % (
                        "->".join( map(unicode, k)), 
                       isinstance( v, ( str, unicode) ) and ( "'%s'" % v ) or repr(v)  
                    ) for k, v in self.as_vector_iter() ] )
                
    def __add__(left1, left2):
        """adder"""
        left1_big = len(left1.keys()) > len(left2.keys())
        bigger = left1_big and left1.copy() or left2.copy()
        smaller = left1_big and left2 or left1
        for k, v in smaller.iteritems():
            if k in bigger.keys():
                bigger.__setitem__(k, bigger[k] + v )
            else:
                bigger.__setitem__(k,  v)
        return bigger
    
    def __iadd__(self, other):
#        print "self %r" % self
#        self = self + other
        #print "other %r" % other
        for k, v in other.iteritems():
            if k in self.keys():
                self[k] +=  v
            else:
                self.__setitem__(k, v)
        #print "self %r" % self
        return self

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
    b.pprint()
    a += b
    for el in iter_object(a):
        print "<%r>" % (el or "",)
    print "%r" % "-".join( [ repr(k) for k,v in a.as_vector_iter() ] )
