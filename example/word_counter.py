#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" parallel wordcounting with VectorDict 
Notice we can also get all first letter count in the same operations
unlike regular word count methods"""

## Making the input
# wget http://www.gutenberg.org/cache/epub/26740/pg26740.txt
# mv pg26740.txt dorian.txt 
# split -l 2125 dorian.txt dorian_splited.


from multiprocessing import Pool
import string
import re
#from codecs import open as open

from vector_dict.VectorDict import VectorDict as vd
FILES = [ "dorian_splited.aa",  "dorian_splited.ab",
        "dorian_splited.ac",  "dorian_splited.ad" ]


def word_count( unicode_file ):

    exclude = set(string.punctuation)
    def clean(exlcude):
        def _clean(word):
            return ''.join(ch for ch in word if ch not in exclude)
        return _clean

    sp_pattern = re.compile( """[\.\!\"\s\-\,\']+""", re.M)
    res = vd( int, {})                                                           
    for line in iter(open(unicode_file ) ):
        for word in map( clean(exclude),  
                map( str.lower, sp_pattern.split(line ))
            ):
            if len(word) > 2 :
                res += vd(int, { 
                    word : 1 ,'begin_with' : 
                        vd(int, { word[0] : 1 }) }
                )
    return res

p = Pool()
result=p.map(word_count, FILES )
reduce(vd.__add__,result)['begin_with'].tprint()

