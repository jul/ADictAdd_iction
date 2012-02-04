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
if __name__ == '__main__':
    unittest.main(verbosity=2)
