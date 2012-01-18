#!/usr/bin/python
# -*- encoding=utf-8 -*-

from vector_dict import VectorDict


def closest_to_one(a_list, **arg):
    return sorted(
        a_list,
        cmp = lambda x, y: cmp(
                abs(x - 1),
                abs(y - 1)
            ),
        **arg
    )


def closest( candidate ):
    cand_vect = string_as_vect(candidate)
    print "** for the word <%s>" % candidate

    print "better cos : "
    print "%r/%s" % sorted(
        [ (w, cand_vect.cos(v)) for w, v in vectors.iteritems() ],
        key = lambda x: x[1], reverse=True
    )[0]

    print "better projection relative to projected: "
    print "%r/%s" % closest_to_one(
        [ (w, cand_vect.dot(v) / ( v.norm() ** 2 ) ) 
            for w, v in vectors.iteritems() ],
        key = lambda x: x[1]
    )[0]
    
    print "better projection relative to candidate : "
    print "%r/%s" % closest_to_one(
        [ (w, cand_vect.dot(v) / ( cand_vect.norm() ** 2 ) ) 
            for w, v in vectors.iteritems() ],
        key = lambda x: x[1]
    )[0]
    print "least difference: "
    print "%r/%s" % sorted(
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
#for k,v in vectors.iteritems():
#    print "%s is " % k 
#    v.pprint()

map( closest, [ u"com", u"misère", u"commis", u"signifiant", u"komisaire",
    u"lol", u"mizerre", u"chromosome", u"noscomiale", u"économique" ] )

