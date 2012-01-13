#!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
import re
from vector_dict import VectorDict, path_from_array

t1 = u"""Je vais à la pêche aux moules moules moules, qui viendras avec moi?"""
t2 = u"""je vais à la pêche électorale aux voies"""
t3 = u"""tous les chemins mènent à Rome"""
t4 = u"""Le je du jeu, Jeune je vois, est il une jeunesse ?"""
t5 = u"""je jeune à jeun, jeu à jouer"""

a = VectorDict( VectorDict , dict() )
def text_grapher(unicode_text):
    return reduce( 
        VectorDict.__add__,  
        map( 
            lambda  string : path_from_array( 
                filter(unicode.isalpha,list(string)) + [ 'weight' , 1 ]
            ),
            map( unicode.lower,re.split("\s",unicode_text )) 
       )
    )
text_grapher(t1).pprint()

print text_grapher(t1).cos(text_grapher(t2))
print text_grapher(t1).cos(text_grapher(t3))

text_grapher(t4).pprint()
print text_grapher(t4).cos(text_grapher(t5))
text_grapher(t5)[u'j'][u'e'][u'u'].pprint()
