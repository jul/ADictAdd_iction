import os
import sys
sys.path += [os.path.dirname( sys.modules[__name__].__file__) + os.sep + '..'  ]
print sys.path[-1]

import unittest
from VectorDict import VectorDict, convert_tree, Path, dot, cos
from Clause import is_leaf, has_type, is_container, anything
from Operation import mul, cast
from math import sqrt
class TestPath(unittest.TestCase):
    def setUp(self):
        self.a_path = Path( [ e for e in  xrange(10 ) ] )
    
    def test_build(self):
        self.assertEqual(
            self.a_path,
            ( 0, 1, 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9)
        )
    def test_startswith(self):
        self.assertEqual(
            self.a_path.startswith( 0, 1 , 2 ),
            True
        )

    def test_endswith(self):
        self.assertEqual(
            self.a_path.endswith( 8, 9),
            True
        )

    def test_contains1(self):
        self.assertEqual(
            self.a_path.contains( 2 , 3 , 4 ),
            True
        )

    def test_contains1(self):
        self.assertEqual(
            self.a_path.contains( 0, 1 , 2 ),
            True
        )
class TestVectorDict(unittest.TestCase):
    
    def setUp(self):
        self.easy = VectorDict( int, dict( x=1, y=1, z=0 ) )
        self.a_tree = dict( 
            a = 1, 
            b = dict( 
                c = 3.0, 
                d = dict( e = True)
            ), 
            point = self.easy 
        )
        self.cplx = convert_tree( self.a_tree )

    def test_convert(self):
        self.assertEqual( convert_tree( { 'a' : { 'b' : 1 } } ) ,
            VectorDict( VectorDict, 
                { 'a' : VectorDict( VectorDict, dict( b = 1 ) ) }
            )
        ) 

    
    def test_add_not_exists(self):
        self.easy += dict( a = 1 )
        self.assertEqual( self.easy['a'] , 1 )
    def test_add_exists(self):
        self.easy += dict( x = 1 )
        self.assertEqual( self.easy['x'] , 2 )
    def test_clause_has_type(self):
        self.assertEqual( 
            has_type(float)(3.0), 
            True)
    def test_is_leaf(self):
        """ we need a is_leaf more specialized must have a bug somewhre
        in find / match_tre
        TODO have one that tells is not vector_dict
        """
        self.assertEqual(
            all( [ is_leaf(e) for e in [ 
                set(), 
                frozenset(),
                list(),
                (e for e in range(0,10)),
                3.0,
                2,
                False,
                "ljlkjkl",
                ]]),
         True
         )
    def test_is_container(self):
        self.assertEqual(
            all( [ is_container(e) for e in [ 
                dict(), 
                set(), 
                frozenset(),
                list(),
                VectorDict(bool, {}),
                (e for e in range(0,10))
                ]]),
         True
         )
    def test_match_tree(self):
        self.assertEqual( 
            self.cplx["b"].match_tree( dict( c= 3.0 ,d = dict( e = True) )),
            True
        ) 
        
    def test_match_tree2(self):
        self.assertEqual( 
            self.cplx.match_tree( dict( 
                b=dict( c= 3.0, d = anything ))),
            True
        ) 
    def test_match_tree3(self):
        self.assertEqual( 
            self.cplx["b"].match_tree( 
                dict( 
                    c= has_type(float) ,
                    d = anything 
            )),
            True
        ) 
    def test_find1(self):
        self.assertEqual( 
            [ e for e in self.cplx.find( lambda p, v: ( 
                not is_leaf(v) and v.match_tree(
                dict( c= has_type(float) , d = is_container   )
                )
            ))  ][0][0], ('b',))

        
    def test_collision_build_path(self):
        self.assertRaises(
            ValueError,
            self.easy.build_path,  'z' , 1  )
    
            
    def test_collision_build_path2(self):
        self.assertRaises(
            ValueError,
            self.cplx.build_path,  'b' , 1  )
    
    def test_build_path(self):
        self.cplx.build_path(  'b' , "new",  "whatever"  )
        self.assertEqual( 
            self.cplx["b"]["new"],
            "whatever")
            
   # def test_add_path(self):
   #     self.cplx.add_path( [  'b' , "new",  "whatever"]  )
   #     self.cplx.add_path( [  'b' , "new",  "whatever"]  )
   #     self.assertEqual( 
   #         self.cplx["b"]["new"],
   #         "whatever" * 2 )
    
    def test_at1(self):
        self.assertRaises( 
            IndexError,
            self.cplx.at, [ 'a', 'b', 'c' ] )
    
    def test_at2_and_ope_mul(self):
        self.assertEqual( 
            self.cplx.at( [ 'b','c' ]) ,
            3.0
        )
    
    def test_at3_and_ope_mul(self):
        self.assertEqual( 
            self.cplx.at( [ 'b','c' ], mul(-1) ),
            -3.0
        )
    
    def test_at4(self):
        self.assertRaises( 
            Exception,
            self.cplx.at,  'a', 'b', 'c'  )
    
    def test_at5_copy(self):
        """not sure I ever used it"""
        self.assertIsNot( 
            self.cplx.at( [ 'b' ], None, True ),
            self.cplx["b"]
        )
    def test_get_at(self):
        self.assertIs(
            self.cplx.at( ['b', 'c' ] ),
            self.cplx.get_at( 'b' , 'c' )
    )


    def test_dot(self):
        self.assertEqual( 
            dot(
                VectorDict( int, dict( x=1 , y=1, z=0) ),
                VectorDict( int, dict( x=1 , y=1, z=1) ),
             ), 
             float( 2.0 )
        )

    def test_cos(self):
        self.assertAlmostEqual( 
            cos(
                VectorDict( int, dict( x=1 , y=0) ),
                VectorDict( int, dict( x=1 , y=1) ),
             ), 
             float( sqrt(2) / 2 )
        )
    
    def test_build_path_collision(self):
        self.easy.build_path( 'ext' , 'y',  1 )
        self.easy.build_path( 'ext' , 'z',  1 )
        self.assertEqual(
            len(self.easy['ext'].keys()), 
            2
        )
    
    def test_imul( self ):

        a_copy = self.easy.copy()
        self.easy *= -1
        self.assertEqual(
            self.easy['x'],
            -a_copy['x']
        )

    def test_bug_1( self ):
        """bug  #1 : * returns a copy where a reference is needed"""
        pt = self.easy
        pt *= -1
        self.assertEqual(
            self.easy,
            pt
        )

    def test_bug_2( self ):
        """bug #2 : self * other without affectation should not modify self.
        """
        self.easy *= -1
        a_copy = self.easy.copy()
        self.easy * a_copy
        self.assertEqual(
            self.easy,
            a_copy
        )

    def test_bug_3( self ):
        """bug  #3 : / returns a copy where a reference is needed"""
        self.easy.prune( 'z' )
        pt = self.easy.at([])
        pt /= -1
        self.assertEqual(
            self.easy,
            pt
        )


    def test_bug_4( self ):
        """bug #4 : self / other without affectation should not modify self.
        """
        self.easy.prune( 'z' )
        self.easy /= -1
        a_copy = self.easy.copy()
        self.easy / a_copy
        self.assertEqual(
            self.easy,
            a_copy
        )
    

    def test_bug_5( self ):
        """bug #5 : int * dict without affectation should not modify self.
        """
        a_copy = self.easy.copy()
        2 * self.easy
        self.assertEqual(
            self.easy,
            a_copy
        )
    
    def test_bug_6( self ):
        """bug #6 : int / dict without affectation should not modify self.
        """
        self.easy.prune( 'z' )
        a_copy = self.easy.copy()
        2.0 / self.easy
        self.assertEqual(
            self.easy,
            a_copy
        )
    def test_union_func_not_ok(self):
        a_lot_of_type= convert_tree( 
            dict( 
                a = "lkjlkjl",
                b = dict( 
                    e = set( [ 1 , 2 , 3 ] ),
                    f = lambda x ,y : 2 * y,
                
                ),
                p = dict(a  = "saint" )
            )
        )
        another_lot = convert_tree( 
            dict( a = "lkjlkjl",
                b = dict( 
                    e = set( [ 1 , 2 , 3 ] ),
                    f = lambda x ,y : 2 * y,
                    g = dict(),
                ),
                pp = dict(a  = "serre" )
            ),
        )
        cl = Exception('CollisionError','')
        
        self.assertRaises(
        Exception,
        a_lot_of_type.union, another_lot
        )
    def test_union_ok( self):
        a_lot_of_type= convert_tree( 
            dict( 
                a = "lkjlkjl",
                b = dict( 
                    e = set( [ 1 , 2 , 3 ] ),
                    f = 123.123123123,
                
                ),
                p = dict(a  = "saint" )
            )
        )
        another_lot = convert_tree( 
            dict( a = "lkjlkjl",
                b = dict( 
                    h = "fuck",
                    i = dict( a = 1 ),
                    e = set( [ 1 , 2 , 3, 5 ] ),
                    f = 123.123123123,
                    g = dict(),
                ),
                pp = dict(a  = "serre" )
            ),
        )
        un= a_lot_of_type.union(another_lot)
        expected = convert_tree( {
    'a' : 'lkjlkjl',
    'p' : {
        'a' : 'saint',
    },
    'pp' : {
        'a' : 'serre',
    },
    'b' : {
        'i' : {
            'a' : 1,
        },
        'e' : set([1, 2, 3, 5]),
        'g' : {
        },
        'f' : 123.123123123,
    },
})

        self.assertEqual( 
            un,
            expected) 
    
    def test_bug_convert_empty_mapping( self ):
        """bug #8 : empty mapping intialisation dont work"""
        bug = convert_tree( dict( a = {} ) )
        expected  = VectorDict(None, {'a': {}})
        
        self.assertEqual( 
            expected,
            bug

        )
    def test_bug_boolean_not_commutative(self):
        """bug #11: a xor b != ! ( a xand b )"""
        a = VectorDict( lambda : False, 
            dict( tt = True, tf = True, ft=False, ff = False, not_in_b=False) 
        )
        b = VectorDict( lambda : False, 
            dict( tt = True, tf = False, ft=True, ff = False, not_in_a = True) 
        )
        self.assertEqual( ( a & b.__not__() ) | ( a.__not__() & b) , 
            ( ( a | b.__not__() ) & ( a.__not__() | b )).__not__() )

if __name__ == '__main__':
    unittest.main(verbosity=2)
