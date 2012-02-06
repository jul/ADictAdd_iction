#!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
"""test for rules of consistency in algebrae
call the script as it is to see the result for various objects
(int, str, list, numpy array, VectorDict)
and rules tested. 

Mainly the tests are coming out of a math book
"""

from copy import deepcopy


from VectorDict import can_be_walked, VectorDict

def try_copy_or_copy(self, src, dst):
    copy = None
    if hasattr(src, "copy"):
        copy = src.copy()
    else:
        copy = deepcopy(src)
    setattr(self, dst, copy)


class ConsistentAlgebrae(object):
    """test wether an addition for two object is consistant"""

    def __init__(self, **kw):
        """
        only method really callable. 
        Arguments : 
            - neutral : neutral element of addition for the object ; 
            - scalar : real, float, or complex (normaly anything that is 1D, 
              and follow algebraic rules);
            - one : an element to test
            - other : other element to test
        
        
        optionnal :
            - other_scalar : real, float, or complex 
              (normaly anything that is 1D, and follow algebraic rules);
            - context : default  "print" make it verbose ;
            - collect_values : default lambda x : x, if testing for conservation
              a lambda fonction for getting the values
        
        """
        self.fail = 0
        self.context= kw.get("context", "print" )
        self.counter = 0
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
        self.other_scalar = kw.get("other_scalar", 4)
        self.collect_values = kw.get("collect_values", lambda x: x)

        self.pre_test()
        self.LesserCommutativity()
        if hasattr(self.one, '__rmul__'):
            self.BetterCommutativity()

        if hasattr(self.one, '__div__'):
            self.EvenBetterCommutativity()

        if can_be_walked(self.one):
            self.Conservation()

        self.finalize()
    
    def EvenBetterCommutativity(self):
        self.test_fraction_consisentcy()
        self.test_div_consisentcy()

    def pre_test(self):
        if "print" == self.context :
            print "\n" + "*" * 50
            print "\ntesting for  %r class\n" % (self._one.__class__.__name__)
            print " a = %r" % self._one
            print " b = %r" % self._other
            print " c = %r" % self._another
            print " an_int = %r " % self.scalar
            print " other_scalar = %r " % self.other_scalar
            print " neutral element for addition is %r " % self._neutral
            print "\n" + "*" * 50



    def finalize(self):
        """success or not ? """
        if "print" == self.context:
            print "*" * 50 + "\n"
            print "%(counter)r/%(success)r" % self.__dict__
            if self.counter  == self.success and self.algebraic_logic:
                print "%r respects the algebraic acceptation of addition" % (
                    self._one.__class__
                )

            else:
                print "%r follows the dutch logic " % (
                self._one.__class__
            )
            print "\n" + "*" * 50
        else:
            print "%(success)d/%(counter)d test passed" % ( self.__dict__ )
            if self.success == self.counter:
                print "test PASSED"
            else: 
                raise Exception("Test Failed")

    def fixture_and_test(method):
        def pprint(self,method, res, left, right):
            print "\ntest #%d" % self.counter
            print method.__doc__
            print "%s is %s" % (method.__name__, res)
            
            if "ko" == res:
                print res
                print "%r != %r " % (left, right)
        def praise(self,method, res, left, right):
            if "ko" == res:
                print "FAIL"
                print "test #%d" % self.counter
                print method.__doc__
                print "%r != %r " % (left, right)
                print "%r" % res
                self.fail += 1

        def reinit_me(self, *a, **kw):
            to_reinit = dict(_one="one",
                             _other="other",
                             _another="another",
                             _neutral="neutral")
            for src, dst in to_reinit.items():
                obj_src = getattr(self, src)
                try_copy_or_copy(self, obj_src, dst)

            res = "Arg : "
            is_equal = False
            (left,right) = (None , None)
            try:
                (left, right) = method(self, *a, **kw)
                if self.equal:
                    is_equal = self.equal(left, right)
                else:
                    is_equal = left == right
                res = is_equal and "ok" or "ko"
            except Exception as e:
                res += "%r" % e
            finally:
                self.counter += 1
                self.success += is_equal and 1 or 0
                if 'print' == self.context:
                    pprint(self, method, res, left, right )
                else:
                    praise(self, method, res, left, right)
        reinit_me.__doc__ = method.__doc__ 
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
    def test_scalar_multiplication(self):
        """ an_int * a = a + ... + a (n times ) """
        left = self.scalar * self.one
        right = self.one
        for i in xrange(self.scalar - 1):
            right = right + self.one
        return (left, right)

    @fixture_and_test
    def test_multiplicative_identity(self):
        """ 1 * a = a """
        return 1 * self.one, self.one

    @fixture_and_test
    def test_associativity(self):
        """( a + b )  + c  = a + ( b + c )"""
        return (
            self.one + (self.other + self.another),
            (self.one + self.other) + self.another
        )

    @fixture_and_test
    def test_div_consisentcy(self):
        """ a * n  / 2  = a + ... + a n /2 times (n beign odd)"""
        right = (self.one * (self.scalar * 2)) / 2
        left = self.one
        for i in xrange(self.scalar - 1):
            left = left + self.one
        return left, right

    @fixture_and_test
    def test_fraction_consisentcy(self):
        """ a  / 2  = .5 * a"""
        ### not implemented because of the float equality shit
        return self.one / 2.0, .5 * self.one


    @fixture_and_test
    def test_multiply_scalar_symmetric(self):
        """ a * other_scalar = other_scalar * a """
        return (
           self.other_scalar * self.one,
           self.one * self.other_scalar
       )
    @fixture_and_test
    def test_multiply_scalar_associativity(self):
        """ ( an_int + other_scalar ) a = an_int * a  + other_scalar * a """
        return (
           (self.scalar + self.other_scalar) * self.one,
           self.scalar * self.one + self.other_scalar * self.one
       )
    @fixture_and_test
    def test_scalar_commutativity(self):
        """ an_int * a = a * an_int """
        return self.scalar * self.one, self.one * self.scalar

    @fixture_and_test
    def test_associativity_scalar_multiplication(self):
        """ ( an_int *  other_scalar ) * a = an_int ( other_scalar * a )"""
        return (
           (self.scalar * self.other_scalar) * self.one,
            self.scalar * (self.other_scalar * self.one))

    @fixture_and_test
    def test_negative(self):
        """ -a = -1 * a """
        return -1 * self.one, self.one.__neg__()

    @fixture_and_test
    def test_substraction(self):
        """ a - b = a + ( -1 * b) """
        return self.one - self.other, self.one + (-1 * self.other)

    @fixture_and_test
    def test_distributivity(self):
        """ an_int ( a + b) = an_int *a + an_int * b """
        return (
            self.scalar * (self.one + self.other),
            self.scalar * self.one + self.scalar * self.other
        )


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
        self.test_multiplicative_identity()
        self.test_scalar_multiplication()
        self.test_scalar_commutativity()
        self.test_negative()
        self.test_associativity_scalar_multiplication()
        self.test_multiply_scalar_associativity()
        self.test_multiply_scalar_symmetric()
        self.test_associativity()
        self.test_substraction()
        self.test_distributivity()
        self.algebraic_logic = True

    def Conservation(self):
        self.conservation()
        self.conservation_neg()

if '__main__' == __name__:

    import os, sys, inspect
    cmd_folder = os.path.abspath(
        os.path.join(
            os.path.split(
                inspect.getfile( inspect.currentframe() )
            )[0] ,
            "."
        )
    )
    if cmd_folder not in sys.path:
       sys.path.insert(0, cmd_folder)

    try:
        from numpy import array as array

        ConsistentAlgebrae(
            neutral=array([0, 0, 0]),
            one=array([1, 2, 3]),
            another=array([5, 2, 3]),
            other=array([3, 4, -1]),
            equal=lambda left, right: (right == left).all(),
            )
    except Exception as e:
        print "only lamers dont use numpy"


    ConsistentAlgebrae(
        neutral=0,
        one=1,
        other=2,
        another=3

        )


    ConsistentAlgebrae(
        neutral=[],
        one=[1],
        other=[2],
        another=[42]
        )

    ConsistentAlgebrae(
        neutral="",
        one="1",
        other="2",
        another="4"
        )

    ConsistentAlgebrae(
        neutral=VectorDict(int, {}),
        one=VectorDict(int, {"one": 1, "one_and_two": 3}),
        other=VectorDict(int, {"one_and_two": - 1, "two": 2}),
        another=VectorDict(int, {"one": 3, 'two':  2, "three": 1}),
        collect_values=lambda x: x.values()
        )

    one = VectorDict(int, {"one": 1, "one_and_two": 12})
    other = VectorDict(int, {"one_and_two": - 9, "two": 2})

    print "just for fun \n\t%r\n\t+\n\t%r\n\t=\n\t%r" % (one, other, one + other)
