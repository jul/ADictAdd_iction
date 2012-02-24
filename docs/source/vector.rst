===========
Vector Dict
===========

Manipulating dict of dict as trees with :

* set operations
* logical operations
* algebraic behaviour 
* tree manipulations
* search operation
* metrics of similarities
* vector algebrae



Helpers
*******

.. autoclass:: vector_dict.VectorDict.tree_from_path

.. autoclass:: vector_dict.VectorDict.convert_tree


.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: tprint, pprint, tformat

Set Operations
**************

.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: intersection, symmetric_difference, union, issubset, issuperset

Logical Operations
******************

.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: __and__, __or__, __not__

Iterators
*********

.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: as_vector_iter, as_row_iter

Accessing and modifying
***********************

.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: at, get_at, prune, find, build_path

Metrics
*******

.. autoclass:: vector_dict.VectorDict.VectorDict
    :members: norm, dot, jaccard, cos


Aliases
*******

.. autoclass:: vector_dict.VectorDict.cos

.. autoclass:: vector_dict.VectorDict.dot


exemples
********

Making map reduce in mongodb fashion
------------------------------------

.. literalinclude:: ../../example/demonstrate.py
   :lines: 20-


Selecting item in a tree
------------------------

.. literalinclude:: ../../example/test_match.py





