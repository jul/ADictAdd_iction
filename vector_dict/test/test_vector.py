import os
import sys
sys.path += [os.path.dirname( sys.modules[__name__].__file__) + os.sep + '..'  ]
print sys.path[-1]

from hack import *
import unittest
from VectorDict import VectorDict, convert_tree
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
    def test_clause(self):
        self.assertEqual( 
            has_type(float)(3.0), 
            True)
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
            ))  ][0][0], ['b'])

            
if __name__ == '__main__':
    unittest.main(verbosity=2)
