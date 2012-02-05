=======
Roadmap
=======


Convention :
************

version x.y.z

- **x** = API change
- **y** = improvement
- **z** = bugfix

Path to world domination :
**************************

v 0.3.0
    adding some easy features
    matrix,
    vector basic operation (get, at, prune, find)

v 0.5.0
    unittest

v 0.7.0 
    fully fonctionnal make chain
    feature freeze

v 0.9.0
    mastering sphinx :) 
    doc from sphinx on reads the doc and pypi

v 1.0.0 
    nice example and polishing
    I level up in python MMORPG and acquire skill «packaging» \o/ 

Personnal wishlist 
******************

coding set operations on vectordict : 
-------------------------------------

- is subset (inverse of match_tree)
- union (raise exception if different value at same path)
- intersection (all path values in both trees) 
- difference (asymetric) all of src tree not in dst

Vector logical operations :
---------------------------

to test : if a binary number is split in key = position, value = bit
Vector logical operations should yield the same result as
logicial_operation(n1, n2)

Since VectorDict are sparse Vector (based on default dict)
it should yield the good result even if all bits are not defined defaulting 
to the factory (obvioulsy 0 should be a sensible choice)


Could we do Ksat ? 


Sparse Matricial operation :
----------------------------

given source path, lambda expression for a value,
yield the result at destination path 
eq : 
union of 
dst.build_path(dst_path + [ f( src.get(src_path ) ) ] ) 
so init of matrix could be : 
mat = Matrix( [ [ src, dst, lambda ] , ....] )
and would be used like 
dst_tree =  mat( src_tree )

Should be better if coded in a tree ... so that I have algebraic operation
on matrix
in the form key ( src, dst ) => lambda 
will have to define + -  on lambda, I guess I could use functionnal

fast tree manipulation :
------------------------

- swap : give source path, destination path swap both values
- prune : delete items at path
- move : give source path, move items at destination raise exception if bad
- copy : duplicate a part of a tree from src to destination
- get : copy value at path


