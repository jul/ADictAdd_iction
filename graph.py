# t!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
import re
from vector_dict import VectorDict, path_from_array, flattening

t1 = u"""Je vais à la pêche aux moules moules moules, qui viendras avec moi?"""
t2 = u"""je vais à la pêche électorale aux voies"""
t3 = u"""tous les chemins mènent à Rome"""
t4 = u"""Le je du jeu, Jeune je vois, est il une jeunesse ?"""
t5 = u"""je jeune à jeun, jeu à jouer"""

a = VectorDict( VectorDict , dict() )
def path_collider(vector, path):
    """adding a path to a vector"""
    path_copy = list(path)
    if not isinstance( vector, VectorDict):
        if len(vector):
            vector = path_from_array( vector + [ "weight" , 1 ])
        else:
            vector = VectorDict( VectorDict, dict() )
    current = vector
    while len(path) :
        current_key = path.pop(0)
        if current_key in current.keys():
            
            current = current[current_key]
            if current.get("weight", False):
                current["weight"]+=1
        else:
            path = [ current_key ] + path
            break
    if len(path):
        vector += path_from_array( path_copy + [ "weight" , 1 ] )
    return vector 

def text_grapher(unicode_text):
    return reduce( 
        path_collider,  
        map( 
                lambda string : filter(unicode.isalpha,list(string)) ,
                map( unicode.lower,re.split("\s",unicode_text )) 
       )
    )
text_grapher(t1).pprint()

print text_grapher(t1).cos(text_grapher(t2))
print text_grapher(t1).cos(text_grapher(t3))

text_grapher(t4).pprint()
print text_grapher(t4).cos(text_grapher(t5))
text_grapher(t5).pprint()
import pydot as pd

graph = pd.Dot(graph_type='digraph',fontsize = 50  )
node = set()
edge = []
label = [] 
for pair in text_grapher(t4).as_row_iter():
    
    path = [ "ROOT" ] +  pair[0] + list( [ pair[1] ] )  
    ## on vire weigth
    path.pop(-2) 
    node = node | set( x for x in flattening(path)  )
    
    label += [ u"->".join(str(x) for x in path ) ]

    while len(path) >= 2:
        if ( path[0:2]) not in edge:
            edge += [ ( path[0:2] ) ]
        path.pop(0)
    
for n in node:
    graph.add_node( pd.Node( n) )
#print "%r" % edge
for e in edge:
#    print "E %r" % e
    arg = dict()
#    if isinstance(e[1],int):
#        arg = dict( label = label.pop(-1))

    graph.add_edge( pd.Edge( e[0], e[1], arrowhead="normal", **arg ))


graph.write_jpeg("there.jpg")
