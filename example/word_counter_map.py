#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" parallel wordcounting with VectorDict 
Notice we can also get all first letter count in the same operations
unlike regular word count methods"""

## Making the input
# wget http://www.gutenberg.org/cache/epub/26740/pg26740.txt
# mv pg26740.txt dorian.txt 
# split -l 2125 dorian.txt dorian_splited.

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


from multiprocessing import Pool
import string
import re
#from codecs import open as open

from vector_dict.VectorDict import VectorDict as vd
FILES = [ "../dorian_splited.aa",  "../dorian_splited.ab",
        "../dorian_splited.ac",  "../dorian_splited.ad" ]

from resource import getrusage, RUSAGE_SELF,RUSAGE_CHILDREN
print getrusage(RUSAGE_SELF|RUSAGE_CHILDREN )

def word_count_map( unicode_file ):

    exclude = set(string.punctuation)
    def clean(exlcude):
        def _clean(word_it):
            for word in word_it:

                yield ''.join(ch for ch in word if ch not in exclude)
        return _clean

    sp_pattern = re.compile( """[\.\!\"\s\-\,\']+""", re.M)
    def split(line_it):
        for line in line_it:
            for word in sp_pattern.split(line):
                yield word.lower()

    def more_than(limit = 2):
        def _more_than(word_it):
            for word in word_it:
                if len(word)> limit:
                    yield word
        return _more_than

    def emit(word_it):
        for word in word_it:

            yield vd(int, { 
                        word : 1 ,
                        'begin_with' : 
                            vd(int, { word[0] : 1 }) ,
                        'has_size' :
                            vd(int, { len(word) : 1 } )
                        
           })

    return reduce( vd.__add__, 
            emit( 
                more_than(2)(
                    clean(exclude)(
                        split(iter(open(unicode_file )))
                    )
                )
            )
        )


p = Pool()
result=p.map(word_count_map, FILES )
result = reduce(vd.__add__,result)
print getrusage(RUSAGE_SELF )
print "Frequency of words begining with"
result['begin_with'].tprint()
result.prune( "begin_with")
print "Repartition of words size"
result['has_size'].tprint()
result.prune( "has_size")

from itertools import islice
print "TOP 40 most used words"
print "\n".join(
     "%10s=%s" % (x, y) for x, y in sorted(result.items(), key=lambda x: x[1],reverse=True)[:40] 
    
)

"""
EXPECTED RESULTS : 
Frequency of words begining with
{
    '\xc3' : 4,
    'r' : 1426,
    'a' : 5372,
    '1' : 10,
    'c' : 2778,
    'b' : 2659,
    'e' : 1420,
    'd' : 2564,
    'g' : 1534,
    'f' : 2647,
    'i' : 942,
    'h' : 5867,
    'k' : 483,
    'j' : 245,
    'm' : 2567,
    'l' : 2706,
    'o' : 1669,
    'n' : 1416,
    'q' : 199,
    'p' : 2173,
    's' : 5434,
    '2' : 2,
    'u' : 407,
    't' : 9255,
    'w' : 5491,
    'v' : 507,
    'y' : 2077,
    'x' : 9,
    'z' : 3,
}
TOP 40 most used words
       the=3786
       and=2216
       you=1446
      that=1362
       was=1083
       his=995
       had=833
      with=661
       him=661
       for=588
      have=561
       not=474
       her=439
       she=431
    dorian=420
      what=399
       but=396
       one=393
       are=372
     there=337
      they=318
     would=308
       all=294
      said=262
       don=255
      from=254
      were=251
      lord=248
     henry=237
      been=236
      life=232
      like=227
       who=224
     about=223
      when=218
      your=207
      some=205
      gray=205
      them=203
      will=201
"""

