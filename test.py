#!/usr/bin/python
#WTFPL

from accu_dict import AccuDict

from copy import deepcopy 

def try_copy_or_copy(self, src, dst ):
    copy = None
    if hasattr( src, "copy"):
        copy = src.copy()
    else:
        copy = deepcopy(src)
    setattr( self, dst,  copy )


class consistent_addition:
    """test wether an addition for two object is consistant"""
    def __init__(self, **kw):

        self.neutral = None
        self.one = None
        self.other = None
        self._neutral = kw["neutral"]
        self._one = kw["one"]
        self._other = self._other = kw["other"]
        self.equal = kw.get( "equal" , None ) 
        print "testing for  %r class %r" % ( self._one.__class__.__name__  , kw )
        self.LesserCommutativity()
        print "******"
    
    def fixture(method):
        def reinit_me(self, *a, **kw ):
            to_reinit =  dict( _one = "one", _other = "other" , _neutral = "neutral" )
            for src, dst in to_reinit.items():
                obj_src = getattr( self, src )
                try_copy_or_copy(self, obj_src, dst )

            res = "Arg" 
            try:
                ( left, right ) = method( self, *a , **kw )
                if self.equal:
                    is_equal =  self.equal( left,   right )
                else:
                    is_equal = left == right
                res = is_equal and "ok" or "ko" 
            except Exception as e:
                res += "%r" % e 
            print "%s is %s" % (method.__name__ , res ) 
        return reinit_me 



    @fixture
    def test_commutativity( self ):
        return ( self.other + self.one ,  self.one + self.other )
   
    @fixture
    def test_neutral( self ):
        return ( self.neutral + self.one , self.one )


    @fixture
    def test_mul_scal(self ):
        return 2 * self.one, self.one + self.one
    
    @fixture
    def test_neutral_mul_scal( self ):
        return self.scal_neutr * self.one, self.one 

    @fixture
    def test_neg(self):
        return -1 * self.one , self.one.__neg__() 

    @fixture
    def test_neg_and_mul(self ):
        return self.one - self.other , self.one + ( - 1 * self.other )

    @fixture
    def test_scal_lin_combo(self):
        return ( 
            self.scalar * ( self.one + self.other ) , 
            self.scalar * self.one + self.scalar * self.other
        )
    
    @fixture
    def conservation(cls):
        return sum( cls.one.values() + cls.other.values() ), sum( cls.one.values() + cls.other.values() )

        
        
    def LesserCommutativity(self ):
        self.test_commutativity()
        self.test_neutral()

    

    def BetterCommutativity( self ):
        if not getattr(self, scal_neutr ):
            print "No way I can test"
        else:
            self.test_neutral_mul_scal()
            self.test_mul_scal()
            self.test_neg()
            self.test_sub()
            

from numpy import array as array

consistent_addition( 
    neutral = array( [ 0, 0, 0 ])  ,
    one = array( [ 1 , 2 , 3 ] ) , 
    other = array( [ 3 , 4 , -1 ] ), 
    equal = lambda left, right : (right == left).all() 
    )

consistent_addition( 
    neutral = 0 , 
    one = 1 , 
    other = 2 )

consistent_addition( 
    neutral = "", 
    one = "1" , 
    other = "2" )

CA = consistent_addition( 
    neutral = AccuDict( int, { } ) , 
    one = AccuDict( int, { "one" : 1 , "one_and_two" : 3 } ),
    other = AccuDict( int, { "one_and_two" : -1, "two":2 } ),
    )
CA.conservation()

one = AccuDict( int, { "one" : 1 , "one_and_two" : 12 } )
other = AccuDict( int, { "one_and_two" : -9, "two":2 } )

print "%r" % (  one + other )
