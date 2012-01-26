#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple test of dictionnary distance with strings being casted as
vectors of letters. And comparaison of misc candidates to the "reference"
3 measures are used : 
cos : aka vectors pointing in the same direction
projection : one vector is projected on another one, and we normalize
on the norm of the reference, the closest to one are best fits
difference : each vectors are substracted and we compare the norms

"""
import os, sys, inspect
cmd_folder = os.path.abspath(
    os.path.join(
        os.path.split(
            inspect.getfile( inspect.currentframe() )
        )[0] ,
        ".."
    )
)
if cmd_folder not in sys.path:
   sys.path.insert(0, cmd_folder)


from vector_dict.VectorDict import VectorDict


def closest_to_one(a_list, **arg):
    """return a sorted
    based on comparing values that are in absolute values 
    the closest to one"""
    return sorted(
        a_list,
        cmp = lambda x, y: cmp(
                abs(x - 1),
                abs(y - 1)
            ),
        **arg
    )


def closest( candidate ):
    """ misc test of distance"""
    cand_vect = string_as_vect(candidate)
    print "** for the word <%s>" % candidate
    
    print "better jaccard similarity : "
    print "%s/%r" % sorted(
        [ (w, cand_vect.jaccard(v)) for w, v in vectors.iteritems() ],
        key = lambda x: x[1], reverse=True
    )[0]


    print "better cos : "
    print "%s/%r" % sorted(
        [ (w, cand_vect.cos(v)) for w, v in vectors.iteritems() ],
        key = lambda x: x[1], reverse=True
    )[0]

    print "better projection relative to projected: "
    print "%s/%r" % closest_to_one(
        [ (w, cand_vect.dot(v) / ( v.norm() ** 2 ) ) 
            for w, v in vectors.iteritems() ],
        key = lambda x: x[1]
    )[0]
    
    print "better projection relative to candidate : "
    print "%s/%r" % closest_to_one(
        [ (w, cand_vect.dot(v) / ( cand_vect.norm() ** 2 ) ) 
            for w, v in vectors.iteritems() ],
        key = lambda x: x[1]
    )[0]
    print "least difference: "
    print "%s/%r" % sorted(
        [ (w, (cand_vect - v).norm() / cand_vect.norm() ) for w, v in vectors.iteritems() ],
        key = lambda x: x[1],

    )[0]
    return True


string_as_vect = lambda string :  reduce( VectorDict.__add__,
	( VectorDict(float,  { unicode(c) : 1.0 } )   for c in string )
)


could_be = [
    u"commisération",
    u"commissaire",
    u"commis",
    u"salopette",
    u"justice",
    u"singulier",
    u"ovni",
    u"sacarstique",
    u"comme",
    u"écnomie",
    u"économe",
    ]


vectors =  dict( ( noun, string_as_vect(noun) ) for noun in could_be )

map( closest, [ u"com", u"misère", u"commis", u"signifiant", u"komisaire",
    u"lol", u"mizerre", u"chromosome", u"noscomiale", u"économique" ] )

