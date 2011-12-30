#!/usr/bin/python
#WTFPL

from accu_dict import AccuDict, can_be_walked

from copy import deepcopy


def try_copy_or_copy(self, src, dst):
    copy = None
    if hasattr(src, "copy"):
        copy = src.copy()
    else:
        copy = deepcopy(src)
    setattr(self, dst, copy)


class consistent_addition(object):
    """test wether an addition for two object is consistant"""

    def __init__(self, **kw):
        self.counter = 1
        self.success = 0 
        self.neutral = None
        self.one = None
        self.other = None
        self.another = None
        self.algebraic_logic = False
        self._neutral = kw["neutral"]
        self._another = kw["another"]
        self._one = kw["one"]
        self._other = self._other = kw["other"]
        self.equal = kw.get("equal", None)
        self.scalar = kw.get("scalar", 3)
        self.other_scalar = kw.get("other_scalar" , 4 )
        self.collect_values = kw.get("collect_values", lambda x: x)
        print "\n" + "*" * 50
        print "\ntesting for  %r class\n" % (self._one.__class__.__name__)
        print " a = %r" % self._one
        print " b = %r" % self._other
        print " c = %r" % self._another
        print " an_int = %r " % self.scalar
        print " other_scalar = %r " % self.other_scalar 
        print " neutral element for addition is %r " % self._neutral
        print "\n" + "*" * 50

        self.LesserCommutativity()
        if hasattr(self.one, '__rmul__'):
            self.BetterCommutativity()

        if can_be_walked(self.one):
            self.Conservation()

    def __del__(self):
        """success or not ? """
        print "*" * 50  + "\n"
        if self.counter - 1 == self.success and self.algebraic_logic :
            print "%r respects the algebraic acceptation of addition" % ( 
                self._one.__class__
            )

        else:
            print "%r follows the dutch logic " % ( 
            self._one.__class__
        )
        print "\n" + "*" * 50

    def fixture_and_test(method):
        def reinit_me(self, *a, **kw):
            to_reinit = dict(_one       = "one",
                             _other     = "other",
                             _another   = "another",
                             _neutral   = "neutral")
            for src, dst in to_reinit.items():
                obj_src = getattr(self, src)
                try_copy_or_copy(self, obj_src, dst)

            res = "Arg : "
            is_equal = False
            try:
                (left, right) = method(self, *a, **kw)
                if self.equal:
                    is_equal = self.equal(left, right)
                else:
                    is_equal = left == right
                res = is_equal and "ok" or "ko"
            except Exception as e:
                res += "%r" % e
            print "\ntest #%d" % self.counter
            print method.__doc__
            print "%s is %s" % (method.__name__, res)
            self.counter += 1
            self.success += is_equal and 1 or 0
            if "ko" == res:
                print "%r != %r " % (left, right)
        return reinit_me

    @fixture_and_test
    def test_commutativity(self):
        """ a + b = b + a """
        return (self.other + self.one, self.one + self.other)

    @fixture_and_test
    def test_neutral(self):
        """ a + neutral = a """
        return (self.neutral + self.one, self.one)

    @fixture_and_test
    def test_mul_scal(self):
        """ an_int * a = a + ... + a (n times ) """
        left = self.scalar * self.one
        right = self.one
        for i in xrange(self.scalar - 1):
            right = right + self.one
        return (left, right)

    @fixture_and_test
    def test_neutral_mul_scal(self):
        """ 1 * a = a """
        return 1 * self.one, self.one

    @fixture_and_test
    def test_add_permut(self):
        """( a + b )  + c  = a + ( b + c )"""
        return ( 
            self.one + ( self.other +  self.another ) , 
            ( self.one + self.other ) + self.another  
        )

    @fixture_and_test
    def test_div_consisentcy(self):
        """ a * n  / 2  = a + ... + a n /2 times (n beign odd)"""
        right = (self.one * (self.scalar * 2)) / 2
        left = self.other
        for i in xrange(self.scalar - 1):
            left = left + self.other
        return left, right

    @fixture_and_test
    def test_fraction_consisentcy(self):
        """ a  / 2  = .5 * a"""
        ### not implemented because of the float equality shit
        return self.one / 2, .5 * self.one

    @fixture_and_test
    def test_other_mul_scal_commut(self):
        """ ( an_int + other_scalar ) a = an_int * a  + other_scalar * a """
        return (
           (  self.scalar + self.other_scalar ) * self.one ,
           self.scalar * self.one + self.other_scalar * self.one 
       )

    @fixture_and_test
    def test_mul_scal_commut(self):
        """ an_int * a = a * an_int """
        return self.scalar * self.one, self.one * self.scalar

    
    @fixture_and_test
    def test_permut_scal_mul(self):
        """ ( an_int *  other_scalar ) * a = an_int ( other_scalar * a )"""
        return ( 
           (  self.scalar * self.other_scalar ) * self.one ,
           self.scalar * ( self.other_scalar * self.one ) )

    @fixture_and_test
    def test_neg(self):
        """ -a = -1 * a """
        return -1 * self.one, self.one.__neg__()

    @fixture_and_test
    def test_sub(self):
        """ a - b = a + ( -1 * b) """
        return self.one - self.other, self.one + (-1 * self.other)

    @fixture_and_test
    def test_scal_lin_combo(self):
        """ an_int ( a + b) = an_int *a + an_int * b """
        return (
            self.scalar * (self.one + self.other),
            self.scalar * self.one + self.scalar * self.other
        )

    @fixture_and_test
    def test_permutation(self):
        """a + b = b + a """
        return (self.one + self.other , self.other + self.one )

    @fixture_and_test
    def conservation(self):
        """sum of the parts = sum of the total"""
        return (
            sum(self.collect_values(self.one + self.other)),
            sum(self.collect_values(self.one)) + \
                sum(self.collect_values(self.other))
       )

    @fixture_and_test
    def conservation_neg(self):
        """sum of the differences == differences of the sum"""
        return (
            sum(self.collect_values(self.one - self.other)),
            sum(self.collect_values(self.one)) - \
                sum(self.collect_values(self.other))
       )

    def LesserCommutativity(self):
        self.test_commutativity()
        self.test_neutral()

    def BetterCommutativity(self):
        self.test_neutral_mul_scal()
        self.test_mul_scal()
        self.test_mul_scal_commut()
        self.test_neg()
        self.test_permutation() 
        self.test_other_mul_scal_commut()
        self.test_permut_scal_mul()
        self.test_add_permut()
        self.test_sub()
        self.test_scal_lin_combo()
        self.algebraic_logic = True

    def Conservation(self):
        self.conservation()
        self.conservation_neg()

try:
    from numpy import array as array

    consistent_addition(
        neutral = array([0, 0, 0]),
        one = array([1, 2, 3]),
        another = array( [ 5, 2 , 3 ] ),
        other = array([3, 4, -1]),
        equal = lambda left, right: (right == left).all(),
        )
except Exception as e:
    print "only lamers dont use numpy"


consistent_addition(
    neutral = 0,
    one = 1,
    other = 2,
    another = 3 
    
    )


consistent_addition(
    neutral = [],
    one = [ 1 ],
    other = [ 2 ],
    another = [ 42 ]
    )

consistent_addition(
    neutral = "",
    one = "1",
    other = "2",
    another = "4"
    )

consistent_addition(
    neutral = AccuDict(int, {}),
    one = AccuDict(int, {"one": 1, "one_and_two": 3}),
    other = AccuDict(int, {"one_and_two": - 1, "two": 2}),
    another = AccuDict( int, { "one": 3 , 'two' :  2 , "three" : 1 } ),
    collect_values = lambda x: x.values()
    )

one = AccuDict(int, {"one": 1, "one_and_two": 12})
other = AccuDict(int, {"one_and_two": - 9, "two": 2})

print "just for fun \n\t%r\n\t+\n\t%r\n\t=\n\t%r" % (one, other, one + other)
