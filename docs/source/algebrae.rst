How to use addition, substraction, division and multiplication
==============================================================


Pretty sanely it is a leaf by leaf operation, and will work as long as element supports the operations.


 >>> from vector_dict.VectorDict import convert_tree, VectorDict,Element,Path
 >>> a = convert_tree(dict(a = dict(aint=1,afloat=2.0  , anarray=[1,2], astring="yo"), c= False))
 >>> (a+a).tprint()
 {
     a = {
         aint = 2,
         anarray = [1, 2, 1, 2],
         astring = 'yoyo',
         afloat = 4.0,
     },
     c = 0,
 }
 >>> (a*2).tprint()
 {
     a = {
         aint = 2,
         anarray = [1, 2, 1, 2],
         astring = 'yoyo',
         afloat = 4.0,
     },
     c = 0,
 }
 >>> (a*a).tprint()
 #Traceback (most recent call last):
 #File "<input>", line 1, in <module>
 #File "vector_dict/VectorDict.py", line 537, in __mul__
 #  return self.__opfactory__(other, True)
 #File "vector_dict/VectorDict.py", line 557, in __opfactory__
 #  return getattr(a_copy, intern_operation)(other)
 #File "vector_dict/VectorDict.py", line 852, in __internal_mul__
 #  new_dict[k] = (self[k]).__internal_mul__( other[k] )
 #File "vector_dict/VectorDict.py", line 854, in __internal_mul__
 #  new_dict[k] = self[k] * other[k]
 #TypeError: can't multiply sequence by non-int of type 'list'


It also works (in the rules of conservation) by creating new path/value in the new tree if it does not exists for addition. In multiplication if values are not present in both trees they are skipped.

 >>> a = convert_tree(dict(a = dict(x=1, y=2.0, z=3), c= 1))
 >>> b = convert_tree(dict(a = dict(x=-1.0, y=2.0, z=6), d= 1))
 >>> (a+b).tprint()
 {
     a = {
         y = 4.0,
         x = 0.0,
         z = 9,
     },
     c = 1,
     d = 1,
 }
 >>> (a*b).tprint()
 {
     a = {
         y = 4.0,
         x = -1.0,
         z = 18,
     },
 }
 >>> (a-b).tprint()
 {
     a = {
         y = 0.0,
         x = 2.0,
         z = -3,
     },
     c = 1,
     d = -1,
 }
 >>> (1.0*a/b).tprint()
 {
     a = {
         y = 1.0,
         x = -1.0,
         z = 0.5,
     },
 }

         

