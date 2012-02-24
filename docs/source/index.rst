.. vector_dict documentation master file, created by
   sphinx-quickstart on Tue Jan 24 16:25:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

References : 
============

* source : https://github.com/jul/ADictAdd_iction/
* online documentation : http://readthedocs.org/docs/vectordict/en/latest/
* ticketing : https://github.com/jul/ADictAdd_iction/issues

What's new in 0.5.0
===================

Partial support for set operation
*********************************

Works only if leaves support the - operation ... :/ (so it shouldn't work with dict including strings or arrays. 

I am working on the algorithm. Consider these as highly experimental, but these will be the exact behaviours and API of the final methods. 

Refactoring + - / * 
*******************

I am currently trying to factor the operations. My brain says there may be a bug. I can't see it yet. 

New doc
*******

More room to the actual useful features. 
And preparing a feature freeze in order to migrate to 1.0.0. Mainly I focus on
QA problems (like better code coverage in unittest). 



Manipulating dict of dict as trees pretty easily
================================================

Contents:


.. toctree::
    vector
    finding
    algebrae
    matrix
    cl_op
    path
    consistent
    roadmap  

  

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

