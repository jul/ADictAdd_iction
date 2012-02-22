
=====================================================
Concept of algebraic algebrae on dict and rooted tree
=====================================================

First of all, this project was a mere intuition that worked, and then I
discovered people liked explantations. So here I try.

The questions are does it makes sense, is it consistent, what we can
expect from this, and then is implementation too complex ? 

Algebrae
========

.. warning:: 
   Of course, I always refer to **linear algebrae** when I say **algebrae** not to
   confuse them. And of course the implicit geometry used for vector is
   euclidian. But shush... Some people still dont know there is much more
   than only euclidian geometry :) 


Algebrae can be defined as an addition anything that follows classical rules :

- existence of a neutral element, 
- distributivity, 
- associativity,
- rules of multiplication by a scalar (notion that is not defined in python :( ),
- commutativity ... 

All theses rules were first implemented as a meta-test. Because
algebrae is like duck typing : if it does everything like an addition
therefore it is one. This is implemented in :ref:`consistency-label`


.. warning:: 
   when I say **tree** I refer to **n-ary rooted tree**, in the limit of
   the contengency made by implementing n-ary rooted trees as a dict of dict


See definition `Definition of Linear Algebrae on Wikipedia
<http://en.wikipedia.org/wiki/Linear_algebra>`_


Homeomorphism between dict and k-ary rooted tree
================================================


Current implementation is simply made by overloading all revelant
operations ( **+ - * /**), and delegating to all the leaf the
operations. If you imbricate VectorDict, you therefore obtain linear
algebrea on n-ary rooted tree. 


Is this legitim ? 

Well I have to primitive to display imbricated VectorDict 

And as you can see, by collapsing a path in the set of keys that leads
to a value I can always find a bijection between a vector and the n-ary
rooted tree obtained. 

Therefore it is legitim.

.. literalinclude:: ../../example/pretty_printing.py

It is the open gates to any matrix ! 
====================================

Well, when you have vector, linear algebrae ... **you have matrix** !

:ref:`matrix-label`

What is a matrix ? 
******************

A matrix takes a vector as an input, and gives a transformed matrix as
an output. 

What's the use
***************

XSLT was all about transforming trees in trees, such as can jquery be
used, such as a parser is. 

Matrices are not as fancy as jquery or Xpath yet for two main reasons : 

* matrices dont make fancy adressing, a matrix is about absolute input  dimension, absolute output dimension and a scalar by wich to multiply the value ; 
* matrices are normally not complicated :) 

I was too lazy to do the normal matrix, I cheated a little bit by
allowing matrix to have matrix as values, and broadened a little
bit the notion of matrix. 

It is simply a convenient way to transform a tree in a tree, and it can be seen as code that can be manipulated (added, or'ed, 
multiplied ...)


Metrics oriented querying
=========================

At one point or another, having metrics on a dict, and with the
increasing use of json/key value based, there will be the use of metrics based query. 

Typically, you'll want any subtree having specific attributes, and
you'll want to fetch it in the map/filter phase if it belongs to a
domain, or close enough to your criterion. Cosinus, jaccard comparison,
norm and doct product will enable all this. 

I am still working on an elegant way of doing this easily in a way that
makes any pythonista eyes bleed as much as possible.

.. warning::
    this was a troll, I have no intention to make anyone's eyes bleed.


Can it be ported ?
==================

As far as I am concerned, for having programmed, or red programming
books concerning the revelant langage it can be easily ported to :

* Perl,
* Ruby,
